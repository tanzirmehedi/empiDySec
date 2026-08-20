# Six malicious PyPI packages that a `pip install` sandbox would have called clean

Most tooling that screens Python packages watches what happens during installation. Run `pip install`, capture the syscalls, flag anything that spawns a shell or opens a socket. It's a reasonable place to look, because that is where the loudest supply-chain attacks live.

It is also where only some of them live.

While building a behavioural benchmark, we went back through packages that carried a *benign* label and looked at them across the whole lifecycle — install, import, and the point where a user actually runs the thing. Six turned out to be malicious. All six have since been removed from PyPI following our reports. What makes them worth writing up is not that they were sophisticated. Most weren't. It's that each one becomes visible at a different moment, and no single observation window catches more than a couple of them.

Here they are, with the moment each one gives itself away:

| Package | Version | Downloads | Becomes visible at | Dominant signal |
|---|---|---|---|---|
| CyberOsint | 0.4 | ~15,000 | user runs it | Process spawn + network I/O |
| discord_command | 0.0.2 | ~150,000 | when something calls it | Network I/O / token exfiltration |
| eth-abcde | 0.2.3 | 479 | first signing operation | State transition + network I/O |
| infoind | 3897 | 848 | import | Obfuscated dynamic execution |
| Pytonlib | 0.0.0 | ~51,235 | install | Install process + remote fetch |
| vermillion | 0.5 | ~2,800 | user runs the dropped binary | File I/O / binary drop |

Only one of those six — Pytonlib — does anything interesting during `pip install`.

---

## The one that behaves like you'd expect

Pytonlib is the textbook case, and it's useful as a baseline. It overrides setuptools' `install` command with a randomly named `cmdclass` entry, so its payload runs during installation, before the victim imports anything. The override checks for Windows, decrypts an embedded Fernet blob, and executes the result. That stage then fetches more code from `funcaptcha.ru` and executes that too. What arrives is chosen by the attacker at request time, so it isn't recoverable from the archive at all.

The name is the whole point: PyPI normalises project names, and `Pytonlib` collides with `pytonlib`, a real and actively maintained TON blockchain client. Anyone typing the wrong capitalisation, or any tool resolving the normalised name, could land here. It also means the download figures under that name are unreliable — the two projects share a namespace.

![Inspector view of Pytonlib's utils/wallet.py, showing base64 wallet-code constants keyed by SHA-256 digest.](Pytonlib_Malicious_Code_jpg.png)

The archive isn't only a payload, either. It carries library code lifted from the real project — here, wallet-version constants and their extractor helpers — which is what makes the collision convincing to anyone who opens the package and skims.

Install-time monitoring catches this one comfortably. Now the other five.

---

## The one that waits for a signing call

`eth-abcde` is a verbatim copy of the legitimate `eth-account` library, right down to the README badges, the Discord invite and the "The Ethereum Foundation" authorship line. Two things were changed. A base64-encoded attacker URL was added as a constant in `_utils/signing.py`, and one line in `account.py` appends raw key material to that decoded URL and issues an HTTP GET. Decoded, it points at `ethmanager.pythonanywhere.com`.

The placement is the clever part. That line sits inside the routine that normalises a private key before use, so it fires on the first signing operation — not on install, not on import — and a module-level flag ensures it only fires once per process. The library otherwise works perfectly. Nothing fails, nothing hangs, and the user's funds leave later.

Its metadata is the tell. The sdist directory is `eth-abcde-0.2.3`, while `PKG-INFO` declares `Name: eth-manager, Version: 0.8.0`, and the project URLs still point at the upstream `eth-account` repository. Three names for one package.

---

## The one that runs on import

`infoind` hides its actual code behind two layers of AES-CBC encryption and recovers the key by brute force: a counter starts at zero and increments, decryption is attempted with each candidate, and the loop stops when the output decodes as valid UTF-8 instead of raising `UnicodeDecodeError`. The recovered plaintext goes straight to `exec()`.

![Inspector view of infoind's osint.py showing the BruteForce key-recovery loop above the embedded AES ciphertext.](infoind_Malicious_Code.png)

Unwrap both layers and you get something almost disappointing — a short script that scrapes Google for download links and shells out to `pip3 install` for its own dependencies. The payload is benign in effect.

We flagged it anyway, and it's catalogued as MAL-2024-11615 in the OSSF malicious-packages dataset. The reason is structural rather than behavioural. The same loader delivers anything; the key isn't in the file, so signature matching on the key gets you nowhere; and source review cannot tell you what will run, because what will run doesn't exist until it's decrypted. Since `__init__.py` re-exports the module, all of that happens the moment someone types `import infoind`.

---

## The one that's a component, not a weapon

`discord_command` has around 150,000 downloads, which puts it in the top 10% of the index. Install it and watch: nothing happens. `setup.py` is clean. `__init__.py` is empty. A sandbox that installs it, imports it, and waits will produce a completely quiet trace.

Its only functional code is a single exported function.

![Inspector view of discord_command's get.py, showing the log() function posting a token embed to a hard-coded Discord webhook.](figures/discord_command_Malicious_Code.png)

`log(token)` takes a Discord token, wraps it in an embed, and posts it to a hard-coded webhook with a spoofed desktop `User-Agent`. The embed footer cheerfully identifies the tool as a token grabber and names its author. Nothing in the package harvests a token — that job belongs to a separate stage that calls this one.

That division of labour is what makes it interesting. Judged in isolation, the package is a function nobody called. Judged as part of a toolkit, it's the exfiltration half of a credential stealer, and a Discord token is a session credential: hold one and you're in the account without the password and without touching 2FA.

---

## The one where the victim isn't the installer

`CyberOsint` isn't a backdoor. It does exactly what it advertises, and that's the problem — the person at risk is whoever gets looked up, not whoever runs `pip install`.

Nothing executes at install time. Everything happens through the `cyberosint` console script, which queries the LeakOsint breach API for names, emails, phone numbers and usernames, alongside IP geolocation and domain lookups. Alongside the search features sit two things that aren't OSINT at all: a routine that floods a target's phone with verification messages by hammering Telegram and Discord auth endpoints, and a Telegram bot that shows a fake "confirm your phone number" prompt and forwards the victim's number, Telegram ID, name and username to the operator.

![Inspector view of CyberOsint's main.py showing the LeakOsint API constant and the ASCII banner advertising the operator's Telegram handle.](figures/CyberOsint_Malicious_Code.png)

Nobody was hiding. The banner advertises the operator's Telegram handle, the menus are in Russian, and the package is authored under the handle *TheCyberStalker*. It's dual-use tooling that stopped bothering to look dual.

There's a detection lesson buried in it, too: this package *does* generate install-time process spawns and network traffic — from ordinary dependency resolution, since it pulls four third-party libraries. An install-time monitor sees activity here and it's the wrong activity. Noise at install, signal much later.

---

## The one that doesn't execute at all

`vermillion` is a 33 MB Windows executable wearing a Python distribution as a coat.

![Inspector view of vermillion's setup.py, showing bot.exe as package data and a console script pointing at a module that doesn't exist.](figures/vermillion_Malicious_Code.png)

`setup.py` ships `bot.exe` as package data and registers a console script pointing at `vermillion.bot:main` — a module the package doesn't contain. The directory holds an empty `__init__.py` and the binary, nothing else. So the installed command is simply broken, and the executable has to be launched by the user or by some follow-up stage.

We didn't detonate the binary, so we can't tell you what it does. It's a stripped PE32 GUI executable with signs of packing and none of the usual PyInstaller, .NET or Nuitka markers. The declared dependencies are `discord` and `discord_webhook`, the classifier is Windows-only, and the description field carries a Discord invite — all consistent with Discord-based command and control, but that's inference from packaging, not from the code.

Which is the honest position to hold. There's no execution to observe, so behavioural analysis has nothing to say. What's left is packaging: a large opaque binary as package data, zero Python logic, and an entry point aimed at a module that isn't there. Any one of those is odd. Together they're enough.

---

## What we took from it

The six cases don't share an indicator. They share the property of being invisible to whichever window you happened to pick.

Install-time tracing catches Pytonlib and misses the rest. Import-time tracing catches infoind. Watching the entry point catches CyberOsint. Watching a signing operation catches eth-abcde. Nothing behavioural catches vermillion, and only static packaging review flags it. And discord_command produces a clean trace under all of them, because it's built to be called by something else.

Two of them — CyberOsint and discord_command — hadn't been reported before. All six went to the PyPI administrators through the *Submit Malware Report* form, which asks for an Inspector link to the specific lines at issue and a written summary of the behaviour. All six were removed.

![The PyPI malware-report submission filed for CyberOsint.](figures/CyberOsint.png)

That form is worth knowing about if you find something. It's a few paragraphs of work, the review turnaround is fast, and it's the difference between one person knowing and the package being gone.

---

**Indicators**

| Package | Indicator | Type |
|---|---|---|
| eth-abcde | `ethmanager.pythonanywhere.com` | Exfiltration endpoint |
| Pytonlib | `funcaptcha.ru/paste2?package=pytyon` | Stage-2 retrieval |
| CyberOsint | `server.leakosint.com`; `~/.cyberosint_config.json` | Breach API; host artefact |
| discord_command | `canary.discord.com` webhook (truncated) | Exfiltration endpoint |
| vermillion | `bot.exe` as package data; `discord.gg` invite in description | Packaging anomaly |
| infoind | `MAL-2024-11615` | OSSF advisory ID |

*All six distributions have been removed from the index. Download figures are from ClickPy, which retains telemetry for withdrawn projects; the Pytonlib count should be read with care, since the normalised name is shared with a legitimate project.*
