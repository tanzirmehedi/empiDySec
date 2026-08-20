# Removed Malicious PyPI Packages - Case Analysis

This directory documents six verified malicious PyPI packages previously labeled benign and later removed from PyPI following our disclosure. For each package, we summarize its metadata, malicious-code execution stage, and observable behavioral channel. These cases show that pip install-only analysis is insufficient, as malicious behavior may emerge during installation, import, or post-installation execution.

---

## 1. Package inventory

**Table 1.** Distribution metadata for the six packages, all since removed from the PyPI index.

| Package | Version | Total downloads | Last update | Platform | Distribution |
|---|---|---|---|---|---|
| [CyberOsint](https://inspector.pypi.io/project/cyberosint/0.4/packages/99/7c/c8a1caf020bc60504b00c5bff7a28ae79d97a5d40d44e068d709dadd298f/CyberOsint-0.4.tar.gz/) | 0.4 | 15,000 | 2024-07-29 | OS Independent | sdist |
| [discord_command](https://inspector.pypi.io/project/discord-command/0.0.2/packages/6c/03/1448a5eeb17d04f2b20be1d4c698296e1ccd42f92a528799398fdf7a191d/discord_command-0.0.2.tar.gz/) | 0.0.2 | 150,000 (top 10%) | 2021-06-16 | OS Independent | sdist |
| [eth-abcde](https://inspector.pypi.io/project/discord-command/0.0.1/packages/6c/03/1448a5eeb17d04f2b20be1d4c698296e1ccd42f92a528799398fdf7a191d/discord_command-0.0.2.tar.gz/) | 0.2.3 | 479 | 2023-09-28 | OS Independent | sdist |
| [infoind](https://inspector.pypi.io/project/infoind/3897/packages/4c/1b/779eeab098e03fe860ad1ae7f026a53e13621de09fb2b940bdde9c05d376/infoind-3897.tar.gz/) | 3897 | 848 | 2023-07-21 | OS Independent | sdist |
| [Pytonlib](https://inspector.pypi.io/project/pytonlib/0.0.1/packages/31/c2/d7786423b1dba56cab1739c7993195246b8043f98ce4bcdb0b47b8a96607/pytonlib-0.0.1.tar.gz/ ) | 0.0.0 | 51,235 | 2024-06-16 | OS Dependent | sdist |
| [vermillion](https://inspector.pypi.io/project/vermillion/0.5/packages/00/e6/67390b9dcf6cd427bf15d9163be3095697a4e32dbc7aaf001deced8cac41/vermillion-0.5.tar.gz/) | 0.5 | 2,800 | 2024-03-02 | OS Dependent | sdist |

Because all six distributions have been removed from the index, the PyPI JSON API no longer serves records for them; download counts are therefore taken from [ClickPy](https://clickpy.clickhouse.com/), which retains historical telemetry for withdrawn projects.

---

## 2. Evasive packages surface through complementary dynamic signals

The six verified malicious packages span different trigger times and observed dominant behavioural channels (Table 2), including process creation, network and file I/O, state transitions, and dynamic execution patterns. Their malicious behaviour becomes observable during installation, import, post-installation, or subsequent execution rather than through a single common indicator. This diversity shows why combining install-time and post-installation traces provides stronger visibility than relying on one behavioural source alone. These behavioural categories also overlap with the influential feature families identified by SHAP and LIME in Section 4.7 of the paper.

**Table 2.** Verified malicious packages carrying benign benchmark labels and their observed dominant evidence. † denotes previously unknown packages removed after disclosure.

| Package | Trigger | Observed dominant signal |
|---|---|---|
| CyberOsint† | install | Process spawn + network I/O |
| discord_command† | post-install | Network I/O + token exfiltration |
| eth-abcde | post-install | State transition + network I/O |
| infoind | import | Obfuscated syscall execution |
| Pytonlib | install | Process + remote fetch |
| vermillion | user-run | File I/O + binary drop |

---

## 3. Static trigger surface

Static inspection of the archives explains the origin of each dynamic signal in Table 2 and clarifies where the two views diverge.

| Package | Mechanism in the archive | Corresponding trace evidence |
|---|---|---|
| Pytonlib | `cmdclass` override on setuptools' `install` command | Payload executes during `pip install`, then fetches a remote stage |
| CyberOsint | No install hook; four third-party runtime dependencies | Install-time process spawn and network I/O arise from dependency acquisition, not from a payload |
| infoind | `__init__.py` re-exports a module that decrypts and `exec()`s its own body | Obfuscated dynamic execution at import |
| eth-abcde | Exfiltration line inside the private-key normalisation routine, guarded by a one-shot flag | State transition followed by a single outbound request on first signing operation |
| discord_command | Exported `log()` function invoked by a separately distributed script | Network I/O to a hard-coded webhook after installation |
| vermillion | 33 MB Windows binary shipped as package data; entry point references a nonexistent module | File I/O and binary drop; no autonomous execution |

Two cases warrant care when interpreting traces. `CyberOsint` contains no installation hook, so its install-time signal reflects ordinary dependency resolution and build subprocesses; the behaviour of interest occurs later, when the `cyberosint` entry point is invoked. `vermillion` executes nothing on its own - its installed console script targets `vermillion.bot:main`, a module absent from the distribution - so the dropped binary is the only evidence available, and attribution of its behaviour requires analysis outside the package lifecycle.

---

## 4. Per-package findings

### CyberOsint 0.4 - functional OSINT tooling (dual-use)

Not a backdoor. The package delivers the capability it advertises, and the party at risk is the person being searched rather than the person installing it.

Nothing executes at install time; all behaviour is reached through the `cyberosint` console entry point. Lookup functions submit a name, email, phone number or username to the LeakOsint breach-data API (`server.leakosint.com`) using a user-supplied token, alongside IP geolocation, domain and MAC-vendor lookups against public services. The package also contains a phone-number harassment routine that repeatedly triggers verification messages by posting a target number to Telegram and Discord authentication endpoints.

**Observed signal:** process spawn and network I/O at install time from dependency acquisition, followed by outbound HTTPS to a breach-aggregation API once the entry point is invoked.

### discord_command 0.0.2 - Discord token exfiltration helper

Steals a user's Discord login token and sends it to an attacker, potentially allowing unauthorized access to the victim's account.

The package does not locate the token itself during installation. Its `log(token)` function accepts a token and transmits it in an HTTP request to a hard-coded attacker Discord webhook; the embed footer is self-labelled as a token grabber. A separate script (`get.py`, distributed outside the archive) is responsible for obtaining the token and calling `log()`. Because a Discord token functions as a session credential, an attacker holding it can access the account without the password or 2FA.

**Observed signal:** post-installation network I/O to the hard-coded webhook, produced only when the companion script drives the exported function; the distribution alone yields a clean trace.

### eth-abcde 0.2.3 - private key exfiltration via typosquat

Steals a user's Ethereum private key and transmits it to an attacker, who can then drain any funds the key controls.

The package is a verbatim copy of the legitimate `eth-account` library, retaining its README, CI and documentation badges, Discord invite, and "The Ethereum Foundation" authorship. Two modifications were introduced: a base64-encoded attacker URL constant in `_utils/signing.py`, and a single line in `account.py` that appends the raw key material to the decoded URL and issues an HTTP GET. The decoded destination is `ethmanager.pythonanywhere.com`. Exfiltration is placed inside the routine that normalises a private key before use, so it fires on the first signing operation, guarded by a module-level flag so it triggers only once per process. The library otherwise functions correctly, so the victim observes no failure.

Metadata is internally inconsistent and useful as a signal: the sdist directory is `eth-abcde-0.2.3`, while `PKG-INFO` declares `Name: eth-manager, Version: 0.8.0` and the project URLs still point at the upstream `eth-account` repository.

**Observed signal:** a state transition on the one-shot guard flag, followed by a single outbound GET to a non-project domain, with key material in the URL path, emitted from within a signing call.

### infoind 3897 - multi-layer obfuscated loader

Flagged for concealment rather than for the payload it carries. The module conceals its real code behind nested encryption and executes it automatically on import.

Each layer embeds an AES-CBC ciphertext and recovers the key by hashing successive integers until the plaintext decodes as valid UTF-8, then passes the result to `exec()`. Unwrapping both layers yields a short script that scrapes Google search results for download links and shells out to `pip3 install` for its own dependencies. Because `__init__.py` re-exports the module, execution occurs on import with no further user action.

The decrypted payload is benign in effect. The security concern is structural: the same loader delivers arbitrary code, the brute-forced key defeats signature matching on the key itself, and source review cannot inspect what will run. Catalogued as **MAL-2024-11615** in the OSSF malicious-packages dataset.

**Observed signal:** obfuscated dynamic execution - `exec()` of decrypted content at import, followed by subprocess invocation of `pip3` and outbound requests to a search engine.

### Pytonlib 0.0.0 - install-time staged downloader

Downloads and executes attacker-controlled code on Windows hosts during installation, granting arbitrary code execution as the installing user.

The package overrides setuptools' `install` command with a randomly named `cmdclass` entry, so the payload runs during `pip install`, before the victim imports anything. The override gates on Windows, decrypts an embedded Fernet blob, and executes the result; that stage retrieves further code from `funcaptcha.ru/paste2?package=pytyon` and executes it in turn. The final payload is chosen by the attacker at request time and is not recoverable from the archive.

The package contains no other code and no cover story - its summary and description are random character strings. It exists solely to exploit PyPI name normalisation against the legitimate `pytonlib` TON blockchain client (a real project, currently at 0.0.72, whose release history begins at 0.0.1 on 2022-04-26). Download totals recorded under this name should therefore be treated cautiously, since the normalised name is shared with the legitimate project.

**Observed signal:** the clearest of the six - installation-process activity during `pip install`, a remote fetch to an unrelated domain, and execution of the response.

### vermillion 0.5 - Binary dropper

Delivers a 33 MB Windows executable to the victim's machine inside a Python distribution that contains no functionality of its own.

Nothing executes during installation. The declared console-script entry point targets `vermillion.bot:main`, but the package directory holds only an empty `__init__.py` and `bot.exe`, so the installed command is broken and the binary must be launched by the user or by a follow-up stage. The binary is a stripped PE32 GUI executable with indications of packing and no PyInstaller, .NET or Nuitka markers; it was not detonated in this study, so its behaviour is not characterised here. The declared dependencies (`discord`, `discord_webhook`) and the Windows-only classifier are consistent with Discord-based command and control, but this is inference from packaging rather than from the binary. The README states only "Under construction! Not ready for use yet!"

**Observed signal:** file I/O and binary drop at installation, with no autonomous execution; behaviour is observable only once the user runs the binary. Detection otherwise rests on packaging anomalies - a large opaque binary shipped as package data, zero Python logic, and an entry point pointing at a nonexistent module.

---

## 5. Indicators of compromise

| Package | Indicator | Type |
|---|---|---|
| eth-abcde | `ethmanager.pythonanywhere.com` | Exfiltration endpoint |
| Pytonlib | `funcaptcha.ru/paste2?package=pytyon` | Stage-2 retrieval |
| CyberOsint | `server.leakosint.com` | Third-party breach API |
| discord_command | Hard-coded Discord webhook (attacker-controlled) | Exfiltration endpoint |
| infoind | `MAL-2024-11615` | OSSF advisory ID |

---
