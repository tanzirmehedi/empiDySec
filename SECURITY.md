# Security Policy

## Supported Versions

empiDySec is a research prototype maintained through its latest codebase. Security updates are applied only to the current repository version.

| Version                      | Supported          |
| ---------------------------- | ------------------ |
| Latest empiDySec codebase    | :white_check_mark: |
| Earlier or modified versions | :x:                |
| Unvalidated environments     | Best effort only   |

## Validated Environment

The complete experimental pipeline was validated using the following environment:

| Component        | Validated configuration            |
| ---------------- | ---------------------------------- |
| Operating system | Ubuntu 22.04 LTS (64-bit)          |
| Processor        | 13th Gen Intel Core i9-13900K      |
| Memory           | 128 GB RAM                         |
| GPU              | NVIDIA RTX A6000 with 48 GB memory |
| Python           | 3.10.20                            |
| Compiler         | GCC 14.3.0                         |
| TensorFlow/Keras | 2.11.0 with CUDA support           |
| Scikit-learn     | 1.2.2                              |
| NumPy            | 1.23.5                             |
| Pandas           | 1.5.3                              |
| SciPy            | 1.9.3                              |
| Matplotlib       | 3.7.1                              |
| Seaborn          | 0.12.2                             |
| Transformers     | 4.38.2                             |
| Joblib           | 1.3.2                              |

Other environments may work but have not been fully validated. Hardware and library differences may affect execution time and numerical reproducibility.

## Reporting a Vulnerability

We take security issues in empiDySec seriously. Please report vulnerabilities privately through GitHub’s private vulnerability-reporting feature, if available, or through the designated private contact provided by the project maintainers.

Relevant vulnerabilities may include:

* arbitrary code execution within repository utilities;
* path traversal or unsafe file handling;
* sandbox escape or containment failure;
* unsafe dependency or model loading;
* exposure of credentials, tokens, or sensitive trace data;
* command injection in execution scripts; and
* weaknesses that compromise the integrity of experimental outputs.

Please include:

* a clear description of the issue;
* the affected file, component, or version;
* the conditions required to reproduce it;
* minimal reproduction steps or a proof of concept;
* the potential security impact; and
* a suggested mitigation, if available.

Do not include real credentials, active secrets, deployable malware, or sensitive third-party data in a report.

## Disclosure Process

After receiving a report, the maintainers will:

1. acknowledge and review the submission;
2. validate the issue and assess its impact;
3. develop an appropriate fix or mitigation;
4. coordinate disclosure with the reporter where appropriate; and
5. publish an update after affected users can apply the mitigation.

Please do not disclose a vulnerability publicly before the investigation is complete and an appropriate mitigation is available.

## Safe Use

empiDySec analyzes potentially malicious Python packages. Users must execute untrusted packages only within disposable, isolated environments with appropriate filesystem, process, resource, and network controls.

Users should:

* never execute untrusted packages directly on a host system;
* avoid providing real credentials, tokens, or personal information;
* restrict and monitor outbound network communication;
* apply execution timeouts and resource limits;
* sanitize traces before sharing or publication; and
* comply with applicable institutional, legal, and ethical requirements.

Potentially malicious package archives and deployable payloads are not distributed through this repository.

## Research Prototype Disclaimer

empiDySec is a research-oriented prototype for studying malicious-package detection from install-time and post-installation behavior. It is not a production-hardened commercial security system and should not be treated as providing complete detection, containment, or prevention guarantees.

The framework is intended to support defensive research and package prioritization for further investigation rather than autonomous blocking or unrestricted execution of untrusted software.
