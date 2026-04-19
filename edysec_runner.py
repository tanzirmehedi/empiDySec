#!/usr/bin/env python3
"""
End-to-end runner for the eDySec repository.

What this script does
---------------------
1. Checks the repository structure and warns about missing key folders/files.
2. Optionally installs dependencies from requirements.txt.
3. Discovers notebooks across nested folders and subfolders.
4. Executes notebooks in the correct phase order.
5. Saves executed notebook copies while preserving the original folder structure.
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence

try:
    import nbformat
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing notebook execution dependencies. Install them first with:\n"
        "  pip install nbformat nbclient jupyter ipykernel"
    ) from exc


PHASE1_NOTEBOOKS = [
    "Phase (i) Data Preparation/Dataset Overview.ipynb",
    "Phase (i) Data Preparation/t-SNE Implementation.ipynb",
]

PHASE2_PRIORITY = [
    "Phase (ii) Feature Selection/Features Selection Overview.ipynb",
]

PHASE4_PRIORITY = [
    "Phase (iv) Stability & Explainability/Explainability Analysis/FLAML DL MLP Combined XAI.ipynb",
    "Phase (iv) Stability & Explainability/Stability Analysis/Stability Analysis.ipynb",
]

FEATURE_METHODS = ["ANOVA", "CORR", "FLAML", "PSO", "WOA"]
TRACE_NAMES = ["Combined", "Filetop", "Install", "Opensnoop", "Pattern", "SysCall", "TCP"]
SKIP_DIR_KEYWORDS = {
    "Evaluation_Outputs",
    "LIME Outputs",
    "SHAP Outputs",
    "Stability Analysis Outputs",
    ".ipynb_checkpoints",
    "__pycache__",
    "venv",
    ".venv",
}


@dataclass
class RunResult:
    notebook: Path
    success: bool
    seconds: float
    error: Optional[str] = None
    output_path: Optional[Path] = None


# ------------------------------
# Utility helpers
# ------------------------------
def build_dataset_sources(repo_root: Path) -> dict[str, Path]:
    """Index dataset CSV files by basename from Phase (i), then from the repo."""
    sources: dict[str, Path] = {}

    dataset_root = repo_root / "Phase (i) Data Preparation" / "QUT-DV25 Dataset"
    if dataset_root.exists():
        for csv_file in sorted(dataset_root.rglob("*.csv")):
            sources[csv_file.name] = csv_file

    # Fallback: if a CSV exists elsewhere (for example generated artifacts), expose it too.
    for csv_file in sorted(repo_root.rglob("QUT-DV25_*_Traces.csv")):
        sources.setdefault(csv_file.name, csv_file)

    return sources


def phase2_notebook_requires_missing_combined(notebook_path: Path, dataset_sources: dict[str, Path]) -> bool:
    if "Phase (ii) Feature Selection" not in str(notebook_path):
        return False
    if "_Combined_" not in notebook_path.name:
        return False
    return "QUT-DV25_Combined_Traces.csv" not in dataset_sources


def stage_dataset_aliases_for_notebook(
    notebook_path: Path,
    dataset_sources: dict[str, Path],
) -> None:
    """Ensure notebooks can resolve bare dataset filenames via local aliases."""
    notebook_dir = notebook_path.parent

    for filename, source in dataset_sources.items():
        target = notebook_dir / filename
        if target.exists() or source.resolve() == target.resolve():
            continue

        try:
            target.symlink_to(source)
        except OSError:
            # Filesystem or permissions may block symlinks; copy as a safe fallback.
            shutil.copy2(source, target)


def log(message: str) -> None:
    print(message, flush=True)


def warn(message: str) -> None:
    print(f"[WARN] {message}", flush=True)


def info(message: str) -> None:
    print(f"[INFO] {message}", flush=True)


def err(message: str) -> None:
    print(f"[ERROR] {message}", flush=True)


def should_skip_path(path: Path) -> bool:
    return any(part in SKIP_DIR_KEYWORDS or any(key in part for key in SKIP_DIR_KEYWORDS) for part in path.parts)


def normalize_method(value: str) -> str:
    value = value.strip()
    if value.lower() == "all":
        return "all"
    for method in FEATURE_METHODS:
        if method.lower() == value.lower():
            return method
    raise ValueError(f"Unsupported method: {value}")


def normalize_trace(value: str) -> str:
    value = value.strip()
    if value.lower() == "all":
        return "all"
    for trace in TRACE_NAMES:
        if trace.lower() == value.lower():
            return trace
    raise ValueError(f"Unsupported trace: {value}")


# ------------------------------
# Environment and structure checks
# ------------------------------
def print_environment_summary(repo_root: Path) -> None:
    info(f"Repository root: {repo_root}")
    info(f"Python executable: {sys.executable}")
    info(f"Python version: {platform.python_version()}")
    info(f"Platform: {platform.platform()}")

    if not (sys.version_info.major == 3 and sys.version_info.minor == 10):
        warn(
            "This project was documented for Python 3.10.x. "
            f"Current version is {platform.python_version()}. Some notebooks may fail."
        )


def validate_repo_structure(repo_root: Path) -> bool:
    required_dirs = [
        repo_root / "Phase (i) Data Preparation",
        repo_root / "Phase (ii) Feature Selection",
        repo_root / "Phase (iii) DL Model Selection & Evaluation",
        repo_root / "Phase (iv) Stability & Explainability",
    ]

    ok = True
    for path in required_dirs:
        if not path.exists():
            err(f"Missing required directory: {path}")
            ok = False

    dataset_dir = repo_root / "Phase (i) Data Preparation" / "QUT-DV25 Dataset"
    if dataset_dir.exists():
        info(f"Found dataset directory: {dataset_dir}")
    else:
        warn(
            "Dataset directory not found at expected location: "
            f"{dataset_dir}\n"
            "The notebooks may fail if they expect this exact path."
        )

    req_file = repo_root / "requirements.txt"
    if req_file.exists():
        info(f"Found requirements file: {req_file}")
    else:
        warn("requirements.txt not found in repo root.")

    return ok


# ------------------------------
# Dependency installation
# ------------------------------
def install_requirements(repo_root: Path, upgrade_pip: bool = False) -> None:
    req_file = repo_root / "requirements.txt"
    if not req_file.exists():
        raise FileNotFoundError(f"requirements.txt not found at {req_file}")

    if not (sys.version_info.major == 3 and sys.version_info.minor == 10):
        raise RuntimeError(
            "Dependency setup requires Python 3.10.x for this repository. "
            "Current interpreter is "
            f"{platform.python_version()} at {sys.executable}.\n"
            "The pinned versions in requirements.txt (for example pandas==1.5.3 and tensorflow==2.11.0) "
            "are not compatible with Python 3.12.\n"
            "Create or activate a Python 3.10 environment, then run setup again."
        )

    if upgrade_pip:
        info("Upgrading pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    info("Bootstrapping packaging tools (pip/setuptools/wheel)...")
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
            "setuptools",
            "wheel",
        ]
    )

    info("Installing repository dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])

    info("Ensuring notebook execution dependencies are available...")
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "nbformat",
            "nbclient",
            "jupyter",
            "ipykernel",
        ]
    )


# ------------------------------
# Notebook discovery
# ------------------------------
def collect_existing_paths(repo_root: Path, relative_paths: Sequence[str]) -> List[Path]:
    results: List[Path] = []
    for rel in relative_paths:
        p = repo_root / rel
        if p.exists():
            results.append(p)
        else:
            warn(f"Notebook not found, skipping: {p}")
    return results


def discover_phase2_notebooks(repo_root: Path, method: str = "all") -> List[Path]:
    base = repo_root / "Phase (ii) Feature Selection" / "Feature Selection Methods"
    notebooks: List[Path] = []

    # Include Phase (ii) overview notebook first.
    notebooks.extend(collect_existing_paths(repo_root, PHASE2_PRIORITY))

    if not base.exists():
        return notebooks

    methods = FEATURE_METHODS if method == "all" else [method]

    for m in methods:
        method_dir = base / m
        if not method_dir.exists():
            warn(f"Missing feature-selection method directory: {method_dir}")
            continue
        for path in sorted(method_dir.rglob("*.ipynb")):
            if should_skip_path(path):
                continue
            notebooks.append(path)

    # Deduplicate while preserving order
    unique: List[Path] = []
    seen: set[Path] = set()
    for nb in notebooks:
        resolved = nb.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(nb)
    return unique


def discover_phase3_notebooks(repo_root: Path, method: str = "all", trace: str = "all") -> List[Path]:
    base = repo_root / "Phase (iii) DL Model Selection & Evaluation"
    if not base.exists():
        return []

    methods = FEATURE_METHODS if method == "all" else [method]
    notebooks: List[Path] = []

    for m in methods:
        method_dir = base / m
        if not method_dir.exists():
            warn(f"Missing model-selection method directory: {method_dir}")
            continue

        if trace == "all":
            search_roots = [method_dir]
        else:
            search_roots = [method_dir / trace]

        for root in search_roots:
            if not root.exists():
                warn(f"Missing trace directory: {root}")
                continue
            for path in sorted(root.rglob("*.ipynb")):
                if should_skip_path(path):
                    continue
                notebooks.append(path)

    return notebooks


def discover_phase4_notebooks(repo_root: Path) -> List[Path]:
    priority = collect_existing_paths(repo_root, PHASE4_PRIORITY)
    seen = {p.resolve() for p in priority}
    base = repo_root / "Phase (iv) Stability & Explainability"
    others: List[Path] = []
    if base.exists():
        for path in sorted(base.rglob("*.ipynb")):
            if should_skip_path(path):
                continue
            if path.resolve() not in seen:
                others.append(path)
    return priority + others


def discover_all_notebooks(repo_root: Path, method: str = "all", trace: str = "all") -> List[Path]:
    notebooks: List[Path] = []
    notebooks.extend(collect_existing_paths(repo_root, PHASE1_NOTEBOOKS))
    notebooks.extend(discover_phase2_notebooks(repo_root, method=method))
    notebooks.extend(discover_phase3_notebooks(repo_root, method=method, trace=trace))
    notebooks.extend(discover_phase4_notebooks(repo_root))

    unique: List[Path] = []
    seen: set[Path] = set()
    for nb in notebooks:
        resolved = nb.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(nb)
    return unique


def discover_by_phase(repo_root: Path, phase: str, method: str = "all", trace: str = "all") -> List[Path]:
    phase = phase.lower()
    if phase == "1":
        return collect_existing_paths(repo_root, PHASE1_NOTEBOOKS)
    if phase == "2":
        return discover_phase2_notebooks(repo_root, method=method)
    if phase == "3":
        return discover_phase3_notebooks(repo_root, method=method, trace=trace)
    if phase == "4":
        return discover_phase4_notebooks(repo_root)
    if phase == "all":
        return discover_all_notebooks(repo_root, method=method, trace=trace)
    raise ValueError(f"Unsupported phase: {phase}")


def filter_notebooks_by_selector(
    repo_root: Path,
    notebooks: Sequence[Path],
    selectors: Sequence[str],
) -> List[Path]:
    """Filter discovered notebooks by filename, partial path, or full path."""
    if not selectors:
        return list(notebooks)

    selected: List[Path] = []
    seen: set[Path] = set()

    candidates: List[str] = []
    if len(selectors) > 1:
        # Supports unquoted multi-word names:
        # run --phase 2 Features Selection Overview.ipynb
        candidates.append(" ".join(selectors).strip())
    candidates.extend(selectors)

    # 1) Direct path matches
    for cand in candidates:
        p = Path(cand)
        for dp in (p, repo_root / p):
            if dp.exists() and dp.suffix.lower() == ".ipynb":
                rp = dp.resolve()
                if rp not in seen:
                    seen.add(rp)
                    selected.append(rp)

    # 2) Match against discovered notebook set
    lowered = [c.lower() for c in candidates if c.strip()]
    for nb in notebooks:
        rel = str(nb.relative_to(repo_root)).lower()
        name = nb.name.lower()
        if any(token == name or token == rel or token in rel for token in lowered):
            rp = nb.resolve()
            if rp not in seen:
                seen.add(rp)
                selected.append(rp)

    if not selected:
        raise ValueError("No notebooks matched selector(s): " + ", ".join(selectors))

    return selected


# ------------------------------
# Execution
# ------------------------------
def build_output_path(repo_root: Path, notebook_path: Path, executed_root: Path) -> Path:
    rel = notebook_path.relative_to(repo_root)
    return executed_root / rel


def execute_notebook(
    notebook_path: Path,
    repo_root: Path,
    kernel_name: str,
    timeout: int,
    executed_root: Optional[Path],
    in_place: bool,
    allow_errors: bool,
) -> RunResult:
    started = time.time()
    output_path: Optional[Path] = None

    try:
        with notebook_path.open("r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        client = NotebookClient(
            nb,
            timeout=timeout,
            kernel_name=kernel_name,
            allow_errors=allow_errors,
            resources={"metadata": {"path": str(notebook_path.parent)}},
        )
        client.execute()

        if in_place:
            output_path = notebook_path
        else:
            if executed_root is None:
                raise ValueError("executed_root must be provided when in_place=False")
            output_path = build_output_path(repo_root, notebook_path, executed_root)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as f:
            nbformat.write(nb, f)

        return RunResult(
            notebook=notebook_path,
            success=True,
            seconds=time.time() - started,
            output_path=output_path,
        )

    except CellExecutionError as exc:
        return RunResult(
            notebook=notebook_path,
            success=False,
            seconds=time.time() - started,
            error=str(exc),
            output_path=output_path,
        )
    except Exception as exc:  # pragma: no cover
        return RunResult(
            notebook=notebook_path,
            success=False,
            seconds=time.time() - started,
            error=f"{type(exc).__name__}: {exc}",
            output_path=output_path,
        )


def write_summary(results: Sequence[RunResult], summary_path: Path) -> None:
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(results),
        "success": sum(1 for r in results if r.success),
        "failed": sum(1 for r in results if not r.success),
        "results": [
            {
                "notebook": str(r.notebook),
                "success": r.success,
                "seconds": round(r.seconds, 2),
                "output_path": str(r.output_path) if r.output_path else None,
                "error": r.error,
            }
            for r in results
        ],
    }
    summary_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_notebooks(
    notebooks: Sequence[Path],
    repo_root: Path,
    kernel_name: str,
    timeout: int,
    executed_root: Optional[Path],
    in_place: bool,
    continue_on_error: bool,
    allow_errors: bool,
    summary_path: Optional[Path],
) -> int:
    if not notebooks:
        warn("No notebooks found for the selected options.")
        return 0

    info(f"Total notebooks selected: {len(notebooks)}")
    results: List[RunResult] = []
    dataset_sources = build_dataset_sources(repo_root)
    combined_warned = False

    for idx, notebook in enumerate(notebooks, start=1):
        rel = notebook.relative_to(repo_root)

        if phase2_notebook_requires_missing_combined(notebook, dataset_sources):
            if not combined_warned:
                warn(
                    "QUT-DV25_Combined_Traces.csv was not found in Phase (i) Data Preparation/QUT-DV25 Dataset "
                    "or elsewhere in the repository. Skipping Phase (ii) Combined notebooks."
                )
                combined_warned = True
            warn(f"Skipping notebook because combined dataset is missing: {rel}")
            continue

        stage_dataset_aliases_for_notebook(notebook, dataset_sources)

        log("-" * 90)
        info(f"[{idx}/{len(notebooks)}] Executing: {rel}")
        result = execute_notebook(
            notebook_path=notebook,
            repo_root=repo_root,
            kernel_name=kernel_name,
            timeout=timeout,
            executed_root=executed_root,
            in_place=in_place,
            allow_errors=allow_errors,
        )
        results.append(result)

        if result.success:
            info(f"Completed in {result.seconds:.2f}s")
            if result.output_path:
                info(f"Saved executed notebook to: {result.output_path}")
        else:
            err(f"Failed after {result.seconds:.2f}s")
            err(result.error or "Unknown error")
            if not continue_on_error:
                warn("Stopping because continue-on-error is disabled.")
                break

    if summary_path is not None:
        write_summary(results, summary_path)
        info(f"Execution summary written to: {summary_path}")

    failures = [r for r in results if not r.success]
    info(f"Run complete. Success: {len(results) - len(failures)}, Failed: {len(failures)}")
    return 1 if failures else 0


# ------------------------------
# CLI
# ------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Set up and run all eDySec Jupyter notebooks while preserving nested folder structure."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--repo-root",
        default=".",
        help="Path to the eDySec repository root. Default: current directory.",
    )

    check_parser = subparsers.add_parser("check", parents=[common], help="Check environment and repository layout.")
    check_parser.add_argument("--json", action="store_true", help="Reserved for future use.")

    setup_parser = subparsers.add_parser("setup", parents=[common], help="Install dependencies.")
    setup_parser.add_argument("--upgrade-pip", action="store_true", help="Upgrade pip before installing packages.")

    run_parser = subparsers.add_parser("run", parents=[common], help="Discover and execute notebooks.")
    run_parser.add_argument("--phase", default="all", choices=["1", "2", "3", "4", "all"], help="Which phase to run.")
    run_parser.add_argument("--method", default="all", help="Feature-selection method: all, ANOVA, CORR, FLAML, PSO, WOA.")
    run_parser.add_argument("--trace", default="all", help="Trace type: all, Combined, Filetop, Install, Opensnoop, Pattern, SysCall, TCP.")
    run_parser.add_argument("--kernel", default="python3", help="Jupyter kernel name. Default: python3")
    run_parser.add_argument("--timeout", type=int, default=7200, help="Per-notebook timeout in seconds. Default: 7200")
    run_parser.add_argument("--dry-run", action="store_true", help="List notebooks without executing them.")
    run_parser.add_argument(
        "--executed-dir",
        default="executed_notebooks",
        help="Directory for saving executed notebook copies when not using --in-place.",
    )
    run_parser.add_argument("--in-place", action="store_true", help="Overwrite original notebooks with executed outputs.")
    run_parser.add_argument("--continue-on-error", action="store_true", help="Continue executing remaining notebooks after a failure.")
    run_parser.add_argument("--allow-errors", action="store_true", help="Keep executing cells inside notebooks even if a cell errors.")
    run_parser.add_argument(
        "--summary",
        default="execution_summary.json",
        help="Path to JSON summary file, relative to repo root unless absolute."
    )
    run_parser.add_argument(
        "notebook",
        nargs="*",
        help="Optional notebook selector(s): filename, partial path, or full path.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()

    if not repo_root.exists():
        err(f"Repository root does not exist: {repo_root}")
        return 2

    if args.command == "check":
        print_environment_summary(repo_root)
        ok = validate_repo_structure(repo_root)
        return 0 if ok else 1

    if args.command == "setup":
        print_environment_summary(repo_root)
        validate_repo_structure(repo_root)
        try:
            install_requirements(repo_root, upgrade_pip=args.upgrade_pip)
        except (RuntimeError, FileNotFoundError) as exc:
            err(str(exc))
            return 2
        except subprocess.CalledProcessError as exc:
            err(f"Dependency installation failed with exit code {exc.returncode}: {exc.cmd}")
            return 1
        info("Setup complete.")
        return 0

    if args.command == "run":
        print_environment_summary(repo_root)
        validate_repo_structure(repo_root)

        try:
            method = normalize_method(args.method)
            trace = normalize_trace(args.trace)
        except ValueError as exc:
            err(str(exc))
            return 2

        notebooks = discover_by_phase(repo_root, phase=args.phase, method=method, trace=trace)

        try:
            notebooks = filter_notebooks_by_selector(repo_root, notebooks, args.notebook)
        except ValueError as exc:
            err(str(exc))
            return 2

        if args.dry_run:
            info(f"Discovered {len(notebooks)} notebook(s):")
            for nb in notebooks:
                try:
                    print(nb.relative_to(repo_root))
                except ValueError:
                    print(nb)
            return 0

        executed_root = None if args.in_place else (repo_root / args.executed_dir).resolve()
        summary_path = Path(args.summary)
        if not summary_path.is_absolute():
            summary_path = repo_root / summary_path

        return run_notebooks(
            notebooks=notebooks,
            repo_root=repo_root,
            kernel_name=args.kernel,
            timeout=args.timeout,
            executed_root=executed_root,
            in_place=args.in_place,
            continue_on_error=args.continue_on_error,
            allow_errors=args.allow_errors,
            summary_path=summary_path,
        )

    err(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
