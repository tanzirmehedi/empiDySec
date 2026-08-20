#!/usr/bin/env python3

from __future__ import annotations

import argparse
import ast
import io
import re
import sys
import tarfile
import tokenize
import warnings
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=SyntaxWarning)


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

DEFAULT_TOP_K = 20
DEFAULT_MAX_SETUP_BYTES = 5 * 1024 * 1024  # 5 MiB safety limit

# Add historical/platform-specific standard-library names that may not
# appear in sys.stdlib_module_names under the Python version running
# this analysis.
LEGACY_OR_PLATFORM_STDLIB = {
    "__future__",
    "distutils",
    "imp",
    "parser",
    "symbol",
    "asyncore",
    "asynchat",
    "cgi",
    "cgitb",
    "chunk",
    "crypt",
    "mailcap",
    "nis",
    "nntplib",
    "ossaudiodev",
    "pipes",
    "sndhdr",
    "spwd",
    "sunau",
    "telnetlib",
    "uu",
    "xdrlib",
    "msilib",
    "msvcrt",
    "winreg",
    "fcntl",
    "grp",
    "pwd",
    "resource",
    "termios",
    "pty",
}

STDLIB = set(getattr(sys, "stdlib_module_names", set()))
STDLIB.update(LEGACY_OR_PLATFORM_STDLIB)


# ---------------------------------------------------------------------
# General utilities
# ---------------------------------------------------------------------

def normalize_archive_name(path: Path) -> str:
    """Remove common compound archive suffixes for a readable package ID."""
    name = path.name
    lower_name = name.lower()

    suffixes = (
        ".tar.gz",
        ".tar.bz2",
        ".tar.xz",
        ".tgz",
        ".tbz2",
        ".txz",
        ".zip",
        ".whl",
        ".egg",
        ".tar",
    )

    for suffix in suffixes:
        if lower_name.endswith(suffix):
            return name[: -len(suffix)]

    return path.stem


def top_level(module_name: str) -> str:
    """Convert requests.sessions or urllib.request to the top-level name."""
    return module_name.split(".", 1)[0] if module_name else module_name


def category_of(module_name: str) -> str:
    """
    Classify a module by name.

    T includes third-party modules, package-local modules, generated modules,
    and names that cannot be verified as part of the running Python version.
    """
    return (
        "S: standard library"
        if module_name in STDLIB
        else "T: third-party/project-local/other"
    )


def decode_python_source(raw: bytes) -> str:
    """Decode Python source using its PEP 263 encoding declaration when present."""
    try:
        encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
        return raw.decode(encoding)
    except (SyntaxError, UnicodeDecodeError, LookupError):
        return raw.decode("utf-8", errors="replace")


def is_setup_py(member_name: str) -> bool:
    """Return True when an archive member's basename is setup.py."""
    normalized = member_name.replace("\\", "/")
    return PurePosixPath(normalized).name.lower() == "setup.py"


# ---------------------------------------------------------------------
# Static import extraction
# ---------------------------------------------------------------------

def imports_from_source(source: str) -> tuple[list[str], str]:
    """
    Extract top-level imported module names without executing source code.

    Returns
    -------
    imports:
        A list preserving raw import occurrences.
    parser:
        "ast", "regex", or "none".
    """
    if not isinstance(source, str) or not source.strip():
        return [], "none"

    modules: list[str] = []

    # Primary parser: Python AST.
    try:
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = top_level(alias.name)
                    if module:
                        modules.append(module)

            elif isinstance(node, ast.ImportFrom):
                # Ignore relative imports such as "from .helpers import x".
                if node.level == 0 and node.module:
                    module = top_level(node.module)
                    if module:
                        modules.append(module)

        return modules, "ast"

    except (SyntaxError, ValueError, TypeError):
        pass

    # Fallback parser for truncated, obfuscated, or non-parseable setup.py files.
    import_pattern = re.compile(
        r"^\s*import\s+([^#;\n]+)",
        flags=re.MULTILINE,
    )

    for match in import_pattern.finditer(source):
        expression = match.group(1)

        # Supports: import os, sys, requests as req
        for item in expression.split(","):
            item = item.strip()
            if not item:
                continue

            module_name = re.split(
                r"\s+as\s+",
                item,
                maxsplit=1,
            )[0].strip()

            if re.fullmatch(r"[A-Za-z_][\w.]*", module_name):
                modules.append(top_level(module_name))

    from_pattern = re.compile(
        r"^\s*from\s+([A-Za-z_][\w.]*)\s+import\b",
        flags=re.MULTILINE,
    )

    for match in from_pattern.finditer(source):
        modules.append(top_level(match.group(1)))

    return modules, "regex" if modules else "none"


# ---------------------------------------------------------------------
# Archive reading
# ---------------------------------------------------------------------

def read_setup_files_from_zip(
    archive_path: Path,
    max_setup_bytes: int,
) -> tuple[list[tuple[str, bytes]], list[dict]]:
    """Read setup.py members from a ZIP-compatible archive without extracting."""
    setup_files: list[tuple[str, bytes]] = []
    issues: list[dict] = []

    with zipfile.ZipFile(archive_path) as archive:
        for member in archive.infolist():
            if member.is_dir() or not is_setup_py(member.filename):
                continue

            if member.file_size > max_setup_bytes:
                issues.append(
                    {
                        "archive": str(archive_path),
                        "member": member.filename,
                        "stage": "read",
                        "issue": (
                            f"setup.py exceeds safety limit "
                            f"({member.file_size:,} bytes)"
                        ),
                    }
                )
                continue

            try:
                setup_files.append(
                    (member.filename, archive.read(member))
                )
            except (RuntimeError, OSError, zipfile.BadZipFile) as exc:
                issues.append(
                    {
                        "archive": str(archive_path),
                        "member": member.filename,
                        "stage": "read",
                        "issue": repr(exc),
                    }
                )

    return setup_files, issues


def read_setup_files_from_tar(
    archive_path: Path,
    max_setup_bytes: int,
) -> tuple[list[tuple[str, bytes]], list[dict]]:
    """Read setup.py members from a TAR-compatible archive without extracting."""
    setup_files: list[tuple[str, bytes]] = []
    issues: list[dict] = []

    with tarfile.open(archive_path, mode="r:*") as archive:
        for member in archive.getmembers():
            if not member.isfile() or not is_setup_py(member.name):
                continue

            if member.size > max_setup_bytes:
                issues.append(
                    {
                        "archive": str(archive_path),
                        "member": member.name,
                        "stage": "read",
                        "issue": (
                            f"setup.py exceeds safety limit "
                            f"({member.size:,} bytes)"
                        ),
                    }
                )
                continue

            extracted = archive.extractfile(member)
            if extracted is None:
                issues.append(
                    {
                        "archive": str(archive_path),
                        "member": member.name,
                        "stage": "read",
                        "issue": "tarfile.extractfile returned None",
                    }
                )
                continue

            try:
                setup_files.append((member.name, extracted.read()))
            except (OSError, EOFError) as exc:
                issues.append(
                    {
                        "archive": str(archive_path),
                        "member": member.name,
                        "stage": "read",
                        "issue": repr(exc),
                    }
                )

    return setup_files, issues


def read_setup_files(
    archive_path: Path,
    max_setup_bytes: int,
) -> tuple[str, list[tuple[str, bytes]], list[dict]]:
    """
    Detect an archive format and return its setup.py members.

    Returns
    -------
    archive_type:
        "zip", "tar", "unsupported", or "error".
    setup_files:
        List of (member path, raw bytes).
    issues:
        Read/detection issues.
    """
    try:
        if zipfile.is_zipfile(archive_path):
            files, issues = read_setup_files_from_zip(
                archive_path,
                max_setup_bytes,
            )
            return "zip", files, issues

        if tarfile.is_tarfile(archive_path):
            files, issues = read_setup_files_from_tar(
                archive_path,
                max_setup_bytes,
            )
            return "tar", files, issues

        return "unsupported", [], []

    except (
        OSError,
        EOFError,
        tarfile.TarError,
        zipfile.BadZipFile,
        PermissionError,
    ) as exc:
        return (
            "error",
            [],
            [
                {
                    "archive": str(archive_path),
                    "member": "",
                    "stage": "archive",
                    "issue": repr(exc),
                }
            ],
        )


# ---------------------------------------------------------------------
# Data analysis
# ---------------------------------------------------------------------

def analyze_archive_folder(
    input_folder: Path,
    max_setup_bytes: int,
) -> dict[str, pd.DataFrame]:
    """Scan every file recursively and analyze setup.py imports."""
    all_files = sorted(
        path
        for path in input_folder.rglob("*")
        if path.is_file()
    )

    document_frequency: Counter[str] = Counter()
    total_occurrences: Counter[str] = Counter()
    setup_file_frequency: Counter[str] = Counter()

    package_module_records: list[dict] = []
    setup_file_records: list[dict] = []
    archive_records: list[dict] = []
    issue_records: list[dict] = []

    supported_archives = 0
    archives_with_setup = 0
    archives_with_imports = 0

    for file_index, archive_path in enumerate(all_files, start=1):
        archive_type, setup_files, issues = read_setup_files(
            archive_path,
            max_setup_bytes,
        )
        issue_records.extend(issues)

        if archive_type == "unsupported":
            continue

        supported_archives += 1
        package_id = normalize_archive_name(archive_path)

        package_imports: list[str] = []
        ast_setup_count = 0
        regex_setup_count = 0
        empty_setup_count = 0

        if setup_files:
            archives_with_setup += 1

        for member_name, raw_source in setup_files:
            source = decode_python_source(raw_source)
            imported_modules, parser = imports_from_source(source)

            if parser == "ast":
                ast_setup_count += 1
            elif parser == "regex":
                regex_setup_count += 1
            else:
                empty_setup_count += 1

            package_imports.extend(imported_modules)
            setup_file_frequency.update(set(imported_modules))

            setup_file_records.append(
                {
                    "package_id": package_id,
                    "archive": str(archive_path),
                    "archive_type": archive_type,
                    "setup_member": member_name,
                    "setup_size_bytes": len(raw_source),
                    "parser": parser,
                    "unique_import_count": len(set(imported_modules)),
                    "total_import_occurrences": len(imported_modules),
                    "imports": "; ".join(sorted(set(imported_modules))),
                }
            )

        unique_package_imports = set(package_imports)

        if unique_package_imports:
            archives_with_imports += 1

        # Package prevalence: each archive contributes at most one vote/module.
        document_frequency.update(unique_package_imports)
        total_occurrences.update(package_imports)

        package_occurrences = Counter(package_imports)

        for module in sorted(unique_package_imports):
            package_module_records.append(
                {
                    "package_id": package_id,
                    "archive": str(archive_path),
                    "module": module,
                    "category": category_of(module),
                    "occurrence_count": package_occurrences[module],
                }
            )

        archive_records.append(
            {
                "package_id": package_id,
                "archive": str(archive_path),
                "archive_type": archive_type,
                "setup_py_count": len(setup_files),
                "ast_parsed_setup_count": ast_setup_count,
                "regex_parsed_setup_count": regex_setup_count,
                "setup_without_detected_imports": empty_setup_count,
                "unique_import_count": len(unique_package_imports),
                "total_import_occurrences": len(package_imports),
                "standard_unique_imports": sum(
                    module in STDLIB
                    for module in unique_package_imports
                ),
                "third_party_or_other_unique_imports": sum(
                    module not in STDLIB
                    for module in unique_package_imports
                ),
                "status": (
                    "imports detected"
                    if unique_package_imports
                    else "setup.py found, no imports detected"
                    if setup_files
                    else "no setup.py found"
                ),
            }
        )

        if file_index % 500 == 0:
            print(f"Checked {file_index:,}/{len(all_files):,} files...")

    denominator = archives_with_setup

    ranking_rows: list[dict] = []
    for rank, (module, package_count) in enumerate(
        document_frequency.most_common(),
        start=1,
    ):
        ranking_rows.append(
            {
                "rank": rank,
                "module": module,
                "category": category_of(module),
                "package_count": package_count,
                "package_share_percent": (
                    100.0 * package_count / denominator
                    if denominator
                    else 0.0
                ),
                "setup_file_count": setup_file_frequency[module],
                "total_occurrences": total_occurrences[module],
                "mean_occurrences_per_importing_package": (
                    total_occurrences[module] / package_count
                    if package_count
                    else 0.0
                ),
            }
        )

    ranking = pd.DataFrame(ranking_rows)
    package_modules = pd.DataFrame(package_module_records)
    setup_files_df = pd.DataFrame(setup_file_records)
    archives_df = pd.DataFrame(archive_records)
    issues_df = pd.DataFrame(issue_records)

    if ranking.empty:
        category_summary = pd.DataFrame(
            columns=[
                "category",
                "distinct_modules",
                "package_module_incidents",
                "raw_occurrences",
                "incident_share_percent",
            ]
        )
    else:
        category_summary = (
            ranking.groupby("category", as_index=False)
            .agg(
                distinct_modules=("module", "nunique"),
                package_module_incidents=("package_count", "sum"),
                raw_occurrences=("total_occurrences", "sum"),
            )
        )
        incident_total = category_summary[
            "package_module_incidents"
        ].sum()
        category_summary["incident_share_percent"] = (
            100.0
            * category_summary["package_module_incidents"]
            / incident_total
            if incident_total
            else 0.0
        )

    summary = pd.DataFrame(
        [
            ("Files visited recursively", len(all_files)),
            ("Supported ZIP/TAR archives", supported_archives),
            ("Archives containing setup.py", archives_with_setup),
            ("Archives with detected imports", archives_with_imports),
            ("Distinct top-level imports", len(document_frequency)),
            (
                "Standard-library modules observed",
                sum(module in STDLIB for module in document_frequency),
            ),
            (
                "Third-party/project-local/other modules observed",
                sum(module not in STDLIB for module in document_frequency),
            ),
            (
                "Package-module incidents",
                sum(document_frequency.values()),
            ),
            ("Raw import occurrences", sum(total_occurrences.values())),
            ("Recorded issues", len(issue_records)),
        ],
        columns=["metric", "value"],
    )

    return {
        "summary": summary,
        "import_frequency": ranking,
        "package_imports": package_modules,
        "archive_summary": archives_df,
        "setup_files": setup_files_df,
        "category_summary": category_summary,
        "issues": issues_df,
    }


# ---------------------------------------------------------------------
# Output tables
# ---------------------------------------------------------------------

def save_tables(
    tables: dict[str, pd.DataFrame],
    output_folder: Path,
) -> None:
    """Write individual CSV files and one multi-sheet Excel workbook."""
    table_folder = output_folder / "tables"
    table_folder.mkdir(parents=True, exist_ok=True)

    for name, dataframe in tables.items():
        dataframe.to_csv(
            table_folder / f"{name}.csv",
            index=False,
            encoding="utf-8-sig",
        )

    workbook_path = output_folder / "setup_import_analysis.xlsx"

    try:
        with pd.ExcelWriter(
            workbook_path,
            engine="openpyxl",
        ) as writer:
            for name, dataframe in tables.items():
                sheet_name = name.replace("_", " ").title()[:31]
                dataframe.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    index=False,
                )

        print(f"Excel workbook: {workbook_path}")

    except ImportError:
        print(
            "openpyxl is not installed, so the Excel workbook was skipped. "
            "Install it with: pip install openpyxl"
        )


# ---------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------

def configure_plot_style() -> None:
    """Set a compact publication-oriented Matplotlib configuration."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": [
                "Times New Roman",
                "Times",
                "DejaVu Serif",
            ],
            "font.size": 8,
            "axes.labelsize": 8.5,
            "axes.titlesize": 9,
            "xtick.labelsize": 7.5,
            "ytick.labelsize": 7.5,
            "legend.fontsize": 7.3,
            "axes.linewidth": 0.8,
            "lines.linewidth": 1.2,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def save_figure(
    figure: plt.Figure,
    figure_folder: Path,
    stem: str,
) -> None:
    """Save each figure as vector PDF/SVG and 600-dpi PNG."""
    figure.savefig(
        figure_folder / f"{stem}.pdf",
        bbox_inches="tight",
        pad_inches=0.03,
    )
    figure.savefig(
        figure_folder / f"{stem}.svg",
        bbox_inches="tight",
        pad_inches=0.03,
    )
    figure.savefig(
        figure_folder / f"{stem}.png",
        dpi=600,
        bbox_inches="tight",
        pad_inches=0.03,
    )
    plt.close(figure)


def plot_top_imports(
    ranking: pd.DataFrame,
    figure_folder: Path,
    top_k: int,
    denominator: int,
) -> None:
    """Horizontal bar chart of the most prevalent setup.py imports."""
    if ranking.empty:
        return

    data = ranking.head(top_k).copy()
    data["code"] = np.where(
        data["category"].str.startswith("S:"),
        "S",
        "T",
    )
    data["display"] = data["module"] + " (" + data["code"] + ")"
    data = data.iloc[::-1].reset_index(drop=True)

    figure, axis = plt.subplots(figsize=(3.35, 4.9))
    bars = axis.barh(
        data["display"],
        data["package_share_percent"],
        height=0.68,
    )

    for bar, code in zip(bars, data["code"]):
        if code == "T":
            bar.set_hatch("///")

    max_share = float(data["package_share_percent"].max())
    axis.set_xlim(0, max(10, np.ceil((max_share + 8) / 10) * 10))
    axis.set_xlabel("Archives importing module (%)")
    axis.set_ylabel("")
    axis.grid(axis="x", linewidth=0.45, alpha=0.30)
    axis.set_axisbelow(True)

    for bar, count, share in zip(
        bars,
        data["package_count"],
        data["package_share_percent"],
    ):
        axis.text(
            share + 0.7,
            bar.get_y() + bar.get_height() / 2,
            f"{share:.1f}% ({count:,})",
            va="center",
            ha="left",
            fontsize=6.4,
        )

    axis.text(
        0,
        -0.11,
        (
            f"N = {denominator:,} archives containing setup.py. "
            "S: standard library; T: third-party/project-local/other."
        ),
        transform=axis.transAxes,
        fontsize=6.2,
        va="top",
    )

    figure.subplots_adjust(
        left=0.31,
        right=0.98,
        top=0.99,
        bottom=0.14,
    )

    save_figure(
        figure,
        figure_folder,
        "figure_1_top_import_prevalence",
    )


def plot_rank_frequency(
    ranking: pd.DataFrame,
    figure_folder: Path,
) -> None:
    """Full rank-frequency curve showing the import long tail."""
    if ranking.empty:
        return

    data = ranking.copy()

    figure, axis = plt.subplots(figsize=(7.0, 2.9))
    axis.plot(
        data["rank"],
        data["package_share_percent"],
        marker="o",
        markersize=2.8,
        markeredgewidth=0.4,
    )
    axis.fill_between(
        data["rank"],
        data["package_share_percent"],
        alpha=0.10,
    )

    positive = data.loc[
        data["package_share_percent"] > 0,
        "package_share_percent",
    ]

    if not positive.empty:
        axis.set_yscale("log")
        axis.set_ylim(
            positive.min() * 0.70,
            positive.max() * 1.55,
        )

    axis.set_xlim(1, len(data))
    axis.set_xlabel("Import rank")
    axis.set_ylabel("Archives importing module (%)")
    axis.grid(axis="both", linewidth=0.45, alpha=0.27)
    axis.set_axisbelow(True)

    candidate_ranks = [
        1,
        2,
        3,
        5,
        10,
        20,
        30,
        40,
        50,
        60,
        len(data),
    ]

    selected_ranks = sorted(
        {
            rank
            for rank in candidate_ranks
            if 1 <= rank <= len(data)
        }
    )

    for index, rank in enumerate(selected_ranks):
        row = data.iloc[rank - 1]
        vertical_offset = 7 if index % 2 == 0 else -11
        final_point = rank == len(data)

        axis.annotate(
            row["module"],
            (
                row["rank"],
                row["package_share_percent"],
            ),
            xytext=(-4 if final_point else 5, vertical_offset),
            textcoords="offset points",
            fontsize=6.5,
            ha="right" if final_point else "left",
            va="bottom" if vertical_offset > 0 else "top",
        )

    axis.text(
        0,
        -0.22,
        (
            "Logarithmic y-axis. Package prevalence is deduplicated "
            "within each archive."
        ),
        transform=axis.transAxes,
        fontsize=6.3,
        va="top",
    )

    figure.subplots_adjust(
        left=0.10,
        right=0.99,
        top=0.98,
        bottom=0.27,
    )

    save_figure(
        figure,
        figure_folder,
        "figure_2_import_rank_frequency",
    )


def plot_cumulative_coverage(
    ranking: pd.DataFrame,
    figure_folder: Path,
) -> None:
    """Cumulative share of package-module incidents represented by top imports."""
    if ranking.empty:
        return

    data = ranking.copy()
    total_incidents = data["package_count"].sum()

    if total_incidents == 0:
        return

    data["cumulative_incident_share"] = (
        100.0
        * data["package_count"].cumsum()
        / total_incidents
    )

    figure, axis = plt.subplots(figsize=(7.0, 2.7))
    axis.plot(
        data["rank"],
        data["cumulative_incident_share"],
        marker="o",
        markersize=2.7,
        markevery=max(1, len(data) // 15),
    )
    axis.fill_between(
        data["rank"],
        data["cumulative_incident_share"],
        alpha=0.10,
    )

    axis.set_xlim(1, len(data))
    axis.set_ylim(0, 102)
    axis.set_xlabel("Number of highest-ranked imports included")
    axis.set_ylabel("Cumulative incident share (%)")
    axis.set_yticks([0, 20, 40, 60, 80, 100])
    axis.grid(axis="both", linewidth=0.45, alpha=0.27)
    axis.set_axisbelow(True)

    for threshold in (80, 90, 95):
        matches = data.loc[
            data["cumulative_incident_share"] >= threshold
        ]
        if matches.empty:
            continue

        row = matches.iloc[0]
        axis.scatter(
            row["rank"],
            row["cumulative_incident_share"],
            s=22,
            zorder=3,
        )
        axis.annotate(
            f"{threshold}% at rank {int(row['rank'])}",
            (
                row["rank"],
                row["cumulative_incident_share"],
            ),
            xytext=(5, -13 if threshold == 90 else 7),
            textcoords="offset points",
            fontsize=6.7,
            va="top" if threshold == 90 else "bottom",
        )

    axis.text(
        0,
        -0.23,
        (
            "An incident is one archive-module pair; an archive may "
            "contribute to several modules."
        ),
        transform=axis.transAxes,
        fontsize=6.3,
        va="top",
    )

    figure.subplots_adjust(
        left=0.10,
        right=0.99,
        top=0.98,
        bottom=0.29,
    )

    save_figure(
        figure,
        figure_folder,
        "figure_3_cumulative_import_coverage",
    )


def plot_category_share(
    category_summary: pd.DataFrame,
    figure_folder: Path,
) -> None:
    """Compare standard-library and third-party/other incident shares."""
    if category_summary.empty:
        return

    data = category_summary.copy()
    data["short_category"] = np.where(
        data["category"].str.startswith("S:"),
        "Standard library (S)",
        "Third-party/local/other (T)",
    )

    figure, axis = plt.subplots(figsize=(3.35, 2.45))
    bars = axis.bar(
        data["short_category"],
        data["incident_share_percent"],
        width=0.60,
    )

    for bar, value in zip(
        bars,
        data["incident_share_percent"],
    ):
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            value + 1.0,
            f"{value:.1f}%",
            ha="center",
            va="bottom",
            fontsize=7,
        )

    axis.set_ylabel("Package-module incidents (%)")
    axis.set_ylim(
        0,
        max(100, data["incident_share_percent"].max() + 10),
    )
    axis.grid(axis="y", linewidth=0.45, alpha=0.28)
    axis.set_axisbelow(True)
    axis.tick_params(axis="x", labelrotation=12)

    axis.text(
        0,
        -0.26,
        (
            "T also includes package-local or unresolved module names; "
            "the category does not imply maliciousness."
        ),
        transform=axis.transAxes,
        fontsize=6.2,
        va="top",
    )

    figure.subplots_adjust(
        left=0.18,
        right=0.98,
        top=0.97,
        bottom=0.32,
    )

    save_figure(
        figure,
        figure_folder,
        "figure_4_import_category_share",
    )


def plot_imports_per_archive(
    archive_summary: pd.DataFrame,
    figure_folder: Path,
) -> None:
    """Distribution of unique setup.py imports per archive."""
    if archive_summary.empty:
        return

    values = archive_summary.loc[
        archive_summary["setup_py_count"] > 0,
        "unique_import_count",
    ]

    if values.empty:
        return

    upper = int(values.quantile(0.99))
    upper = max(upper, int(values.max() if len(values) < 100 else 1))

    display_values = values.clip(upper=upper)
    bins = min(30, max(5, int(display_values.nunique())))

    figure, axis = plt.subplots(figsize=(3.35, 2.55))
    axis.hist(
        display_values,
        bins=bins,
        edgecolor="black",
        linewidth=0.45,
    )

    median = float(values.median())
    axis.axvline(
        median,
        linestyle="--",
        linewidth=0.9,
        label=f"Median = {median:.0f}",
    )

    axis.set_xlabel("Unique imports per archive")
    axis.set_ylabel("Number of archives")
    axis.grid(axis="y", linewidth=0.45, alpha=0.28)
    axis.set_axisbelow(True)
    axis.legend(frameon=False)

    if values.max() > upper:
        note = f"Values above the 99th percentile are clipped at {upper}."
    else:
        note = "All observed archives are shown."

    axis.text(
        0,
        -0.22,
        note,
        transform=axis.transAxes,
        fontsize=6.2,
        va="top",
    )

    figure.subplots_adjust(
        left=0.18,
        right=0.98,
        top=0.97,
        bottom=0.29,
    )

    save_figure(
        figure,
        figure_folder,
        "figure_5_unique_imports_per_archive",
    )


def generate_figures(
    tables: dict[str, pd.DataFrame],
    output_folder: Path,
    top_k: int,
) -> None:
    """Generate all analysis figures."""
    configure_plot_style()

    figure_folder = output_folder / "figures"
    figure_folder.mkdir(parents=True, exist_ok=True)

    archive_summary = tables["archive_summary"]
    denominator = int(
        (archive_summary["setup_py_count"] > 0).sum()
    ) if not archive_summary.empty else 0

    plot_top_imports(
        tables["import_frequency"],
        figure_folder,
        top_k,
        denominator,
    )
    plot_rank_frequency(
        tables["import_frequency"],
        figure_folder,
    )
    plot_cumulative_coverage(
        tables["import_frequency"],
        figure_folder,
    )
    plot_category_share(
        tables["category_summary"],
        figure_folder,
    )
    plot_imports_per_archive(
        archive_summary,
        figure_folder,
    )


# ---------------------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------------------

def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze imports in setup.py files stored inside Python "
            "package archives."
        )
    )

    parser.add_argument(
        "input_folder",
        type=Path,
        help="Folder containing package archives; subfolders are visited.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Output folder. Default: "
            "<input_folder>/setup_import_analysis_results"
        ),
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help=f"Number of imports in the top-import figure (default: {DEFAULT_TOP_K}).",
    )

    parser.add_argument(
        "--max-setup-mb",
        type=float,
        default=DEFAULT_MAX_SETUP_BYTES / (1024 * 1024),
        help="Maximum setup.py member size to read in MiB (default: 5).",
    )

    return parser.parse_args(argv)


def run_analysis(
    input_folder: str | Path,
    output_folder: str | Path | None = None,
    top_k: int = DEFAULT_TOP_K,
    max_setup_mb: float = DEFAULT_MAX_SETUP_BYTES / (1024 * 1024),
) -> dict[str, pd.DataFrame]:
    """Run the full archive analysis from Python or Jupyter."""
    input_folder = Path(input_folder).expanduser().resolve()

    if not input_folder.exists():
        raise FileNotFoundError(
            f"Input folder does not exist: {input_folder}"
        )
    if not input_folder.is_dir():
        raise NotADirectoryError(
            f"Input path is not a folder: {input_folder}"
        )
    if top_k < 1:
        raise ValueError("top_k must be at least 1.")
    if max_setup_mb <= 0:
        raise ValueError("max_setup_mb must be positive.")

    output_folder = (
        Path(output_folder).expanduser().resolve()
        if output_folder is not None
        else input_folder / "setup_import_analysis_results"
    )
    output_folder.mkdir(parents=True, exist_ok=True)

    max_setup_bytes = int(max_setup_mb * 1024 * 1024)

    print(f"Input folder : {input_folder}")
    print(f"Output folder: {output_folder}")
    print("Scanning archives without extracting them...\n")

    tables = analyze_archive_folder(
        input_folder,
        max_setup_bytes,
    )
    save_tables(
        tables,
        output_folder,
    )
    generate_figures(
        tables,
        output_folder,
        top_k,
    )

    print("\nAnalysis summary")
    print(tables["summary"].to_string(index=False))
    print(
        "\nImportant interpretation:\n"
        "  S = Python standard-library module.\n"
        "  T = third-party, project-local, generated, or unresolved module.\n"
        "  T does not mean malicious.\n"
        "  Only setup.py imports are analyzed."
    )
    print(f"\nResults written to: {output_folder}")
    return tables


def main(argv: list[str] | None = None) -> None:
    """Command-line entry point."""
    args = parse_arguments(argv)
    run_analysis(
        input_folder=args.input_folder,
        output_folder=args.output,
        top_k=args.top_k,
        max_setup_mb=args.max_setup_mb,
    )


if __name__ == "__main__":
    main()
