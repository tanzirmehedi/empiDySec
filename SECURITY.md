# Security Policy

## Supported Versions

empiDySec is a research prototype developed for reproducible malicious-package detection experiments. Maintenance and security fixes are focused on the latest repository version. Earlier versions, modified implementations, and unvalidated environments are not guaranteed to receive security updates.

| Version                      | Supported          |
| ---------------------------- | ------------------ |
| Latest empiDySec codebase    | :white_check_mark: |
| Earlier or modified versions | :x:                |
| Unvalidated environments     | Best effort only   |

Security support is provided on a best-effort basis and does not constitute a production security guarantee.

## Validated Environment

The experimental pipeline was evaluated using the following configuration:

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

Other environments may function but have not been fully validated. Differences in hardware, dependencies, and GPU execution may affect runtime and numerical reproducibility.

## Reporting a Vulnerability

We welcome responsible reports of security vulnerabilities affecting empiDySec.

Please submit vulnerabilities privately through GitHub's private vulnerability-reporting feature, if enabled, or through the designated private contact provided by the project maintainers.

Relevant vulnerabilities include:

- Arbitrary code execution in repository utilities.
- Path traversal or unsafe file handling.
- Sandbox escape or containment failures.
- Unsafe dependency, checkpoint, or model loading.
- Exposure of credentials, tokens, or sensitive trace data.
- Command injection in execution scripts.
- Unauthorized network activity caused by repository utilities.
- Vulnerabilities compromising experimental integrity or reproducibility.

A vulnerability report should include:

1. A clear description of the issue.
2. The affected component, file, or version.
3. The conditions required to reproduce the vulnerability.
4. Minimal reproduction steps or a proof of concept.
5. The potential security impact.
6. A suggested mitigation, if available.

Do not include active credentials, personal information, deployable malware, or sensitive third-party data.

Researchers should avoid performing vulnerability testing against infrastructure they do not own or have authorization to assess.

## Vulnerability Handling and Disclosure

After receiving a vulnerability report, the maintainers will:

1. Acknowledge receipt and review the submission.
2. Investigate and validate the reported issue.
3. Assess its severity and potential impact.
4. Develop an appropriate fix or mitigation where feasible.
5. Coordinate disclosure with the reporter when appropriate.
6. Publish a security update or advisory when a mitigation becomes available.

Response and remediation timelines depend on the severity, reproducibility, and available maintenance resources.

Reporters are encouraged to allow reasonable time for investigation and coordinated disclosure before publicly releasing vulnerability details.

## Safe Use and Execution Containment

empiDySec analyzes potentially malicious Python packages using installation and post-installation behavioral traces. Executing untrusted software carries inherent security risks, even within isolated environments.

All package execution should take place in disposable, appropriately isolated sandboxes with restricted filesystem, process, resource, and network privileges.

Users should:

- Never execute untrusted packages directly on production systems or personal workstations.
- Use disposable execution environments restored from clean base images.
- Restrict filesystem permissions and process privileges.
- Apply execution timeouts and resource limits.
- Avoid supplying real credentials, API keys, tokens, or personal information.
- Restrict, monitor, and log outbound network communication.
- Prevent unnecessary access to internal networks and sensitive infrastructure.
- Terminate remaining processes and discard execution environments after analysis.
- Sanitize collected traces before storage, sharing, or publication.
- Follow applicable institutional, legal, and ethical requirements.

The study used a 120-second sandbox execution budget and monitored outbound communication to observe potentially malicious network behavior.

**Important:** Monitored network access does not eliminate the risk of external communication with attacker-controlled infrastructure. Users reproducing the experiments must assess and control network egress according to their institutional security policies.

The framework does not guarantee complete containment of arbitrary malicious software.

## Adversarial Evaluation

empiDySec includes research experiments investigating package-realizable adversarial transformations and adversarial training.

The evaluated import-padding transformations were designed to modify observable execution behavior while assessing whether the original malicious disruption remained observable.

Three predefined configurations were evaluated:

- Standard-Library.
- Third-party.
- Combined.

Adversarial variants were constructed and executed exclusively within controlled research environments.

Users must not upload adversarial variants to PyPI or other public package registries, distribute modified malicious packages, or deploy transformations against systems without authorization.

The replication repository provides research results and derived behavioral evidence rather than a deployable malware-evasion toolkit.

The reported robustness findings apply to the evaluated transformations and disruption-based packages. They do not establish protection against all adversarial strategies, feature-aware attacks, or previously unseen transformations.

## Data Handling and Artifact Release

The replication repository provides non-sensitive artifacts intended to support independent verification of the reported experiments.

Released materials may include:

- Processed behavioral representations.
- Extracted features and selected feature sets.
- Experimental configurations and model parameters.
- Training and evaluation outputs.
- Statistical analyses and visualizations.
- SHAP and LIME explanation results.
- Sanitized behavioral traces and verification evidence.
- Responsible-disclosure and package-removal records.

Potentially malicious package archives, executable payloads, and deployable adversarial variants are not redistributed.

Before publication, collected evidence should be reviewed and sanitized to remove:

- Credentials and authentication tokens.
- Personal or identifying information.
- Sensitive filesystem paths.
- Private network identifiers where necessary.
- Secrets observed in execution traces or retrieved payloads.
- Other information that could create unnecessary security or privacy risks.

Users must independently assess whether additional sanitization is required before redistributing derived artifacts.

## Reporting Malicious PyPI Packages

Security vulnerabilities in empiDySec and malicious packages discovered through empiDySec are handled through separate reporting processes.

Vulnerabilities affecting the empiDySec framework should be reported privately to the project maintainers.

Suspected malicious PyPI packages should be reported through the appropriate PyPI security-reporting channels.

Reports should contain sufficient technical evidence for investigation, such as:

- Package name and affected version.
- Observed malicious behavior.
- Relevant installation or execution triggers.
- Process, filesystem, or network evidence.
- Retrieved payload information, where appropriate.
- Supporting sanitized execution traces.

Researchers should avoid publicly releasing sensitive exploitation details before affected packages have been investigated and appropriate mitigation or removal has occurred.

During the reported study, two previously unknown malicious packages were identified through QUT-DV25 benchmark-label verification, while four additional malicious packages were identified during independent evaluation of 222 recent PyPI packages.

These findings were reported through responsible-disclosure procedures, and the six identified packages were subsequently removed from PyPI.

## Research Scope and Limitations

empiDySec is a research-oriented framework for evaluating malicious-package detection using dynamic behavioral evidence.

Its primary evaluation targets Linux-based Python packages and combines installation and post-installation traces.

Users should consider the following limitations:

- Dynamic analysis cannot guarantee observation of delayed, interactive, or environment-dependent malicious behavior.
- Linux-based execution may not expose Windows-specific or other platform-dependent payloads.
- Detection performance may differ across package ecosystems, attack families, and future software distributions.
- Reported robustness results do not cover all possible adversarial transformations.
- Explanation agreement and feature sensitivity do not establish causal importance.
- Benchmark accuracy and projected alert precision do not guarantee equivalent deployment performance.
- Model predictions require appropriate investigation before security actions are taken.

Consequently, empiDySec should complement existing package-security checks rather than replace independent verification or production security controls.

## Responsible Research

empiDySec is intended exclusively for defensive cybersecurity research, reproducible experimentation, and the investigation of software supply-chain threats.

Users are responsible for ensuring that their activities comply with applicable laws, institutional policies, ethical requirements, and the terms of any analyzed package repositories.

The project does not authorize:

- Unauthorized testing of third-party systems.
- Distribution of malicious or weaponized packages.
- Deployment of adversarial transformations for malicious purposes.
- Collection or disclosure of third-party secrets.
- Use of the framework to compromise software supply chains.

## Research Prototype Disclaimer

empiDySec is an experimental research prototype and has not been independently certified as a production security system.

The maintainers do not guarantee:

- Detection of every malicious package.
- Prevention of arbitrary code execution or sandbox escape.
- Complete protection against adversarial attacks.
- Compatibility with every environment or package ecosystem.
- Identical numerical results across hardware and software configurations.

The framework is intended to support defensive experimentation, reproducible evaluation, and evidence-driven investigation.

**Detection results should be used to prioritize human review rather than as the sole basis for autonomous package blocking or other high-impact security decisions.**
