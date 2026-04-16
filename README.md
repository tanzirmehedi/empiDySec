### eDySec: A Deep Learning-based Explainable Dynamic Analysis Framework for Detecting Malicious Packages in the PyPI Ecosystem

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

<div align="center">

<!-- Replace these with your real badges -->

<img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
<img src="https://img.shields.io/badge/Platform-Linux-success.svg" alt="Platform">
<img src="https://img.shields.io/badge/Focus-PyPI%20Malware%20Detection-critical.svg" alt="Focus">
<img src="https://img.shields.io/badge/Analysis-Dl-Based Dynamic%20Behavioral-orange.svg" alt="Analysis">
<img src="https://img.shields.io/badge/Stability-Statistical-purple.svg" alt="Stability">
<img src="https://img.shields.io/badge/XAI-SHAP%20%7C%20LIME-purple.svg" alt="XAI">
<img src="https://img.shields.io/badge/Status-Research%20Prototype-informational.svg" alt="Status">

<br><br>

**eDySec** is an explainable deep learning-based dynamic behavioral analysis framework designed to detect malicious Python packages in the **PyPI ecosystem** by monitoring **install-time** and **post-installation** runtime behavior.

Unlike approaches that rely only on static code artifacts or package metadata, eDySec directly observes behavioral signals generated during execution, enabling it to capture **staged payloads**, **runtime-triggered actions**, **environment-aware logic**, and other malicious behaviors that may remain hidden before execution.

</div>

---

## Visual Overview

<p align="center">
  <img src="docs/images/edysec-banner.png" alt="eDySec banner" width="100%">
</p>

<p align="center">
  <em>Replace <code>docs/images/edysec-banner.png</code> with your main project banner or graphical abstract.</em>
</p>

### Demo Animation

<p align="center">
  <img src="docs/animations/edysec_pipeline.gif" alt="eDySec pipeline animation" width="90%">
</p>

<p align="center">
  <em>Add a short GIF showing the end-to-end workflow: trace collection → feature engineering → feature selection → model inference → explanation.</em>
</p>

---

## Table of Contents

* [Why eDySec?](#why-edysec)
* [Key Highlights](#key-highlights)
* [Framework Overview](#framework-overview)
* [Architecture](#architecture)
* [Dataset](#dataset)
* [Trace Categories](#trace-categories)
* [Methodology](#methodology)

  * [1. Data Preparation](#1-data-preparation)
  * [2. Feature Selection](#2-feature-selection)
  * [3. Deep Learning Model Evaluation](#3-deep-learning-model-evaluation)
  * [4. Stability and Explainability](#4-stability-and-explainability)
* [Performance Summary](#performance-summary)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Outputs](#outputs)
* [Explainability](#explainability)
* [Reproducibility](#reproducibility)
* [Limitations](#limitations)
* [Roadmap](#roadmap)
* [Citation](#citation)
* [Acknowledgment](#acknowledgment)
* [License](#license)

---

## Why eDySec?

Software supply-chain attacks have become increasingly stealthy and adaptive. In the PyPI ecosystem, malicious packages often use:

* install-time execution,
* delayed payload activation,
* dependency-triggered behavior,
* dynamic code generation,
* environment-aware checks,
* remote command-and-control communication, and
* post-installation persistence or exfiltration logic.

These behaviors are difficult to identify reliably using only **static analysis** or **metadata inspection**. eDySec addresses this gap by focusing on **what a package actually does at runtime**, rather than only what it appears to contain before execution.

---

## Key Highlights

* **Dynamic behavioral malware detection** for PyPI packages.
* Monitors both **installation** and **post-installation** execution phases.
* Captures runtime evidence using **eBPF-based behavioral tracing**.
* Supports multiple behavioral modalities, including file, process, syscall, and network-related traces.
* Uses **feature selection** to reduce high-dimensional behavioral representations into compact, discriminative subsets.
* Evaluates **nine deep learning models** across classical, pre-attention, and attention-based families.
* Provides **explainability** using **SHAP** and **LIME**.
* Includes **stability analysis** to assess robustness beyond single-run performance.
* Achieves strong accuracy with a substantially reduced feature set and significantly lower false positive and false negative rates than the DySec baseline.

---

## Framework Overview

At a high level, eDySec consists of four tightly connected phases:

1. **Dynamic trace collection** from package execution.
2. **Behavioral feature preparation and transformation**.
3. **Feature subset optimization and deep learning-based detection**.
4. **Explainability and stability analysis**.

<p align="center">
  <img src="docs/images/edysec-overview.png" alt="eDySec framework overview" width="95%">
</p>

<p align="center">
  <em>Suggested figure: a 4-phase pipeline diagram showing runtime traces flowing into preprocessing, feature selection, model evaluation, and XAI/stability modules.</em>
</p>

---

## Architecture

### End-to-End Pipeline

```text
PyPI Package
    │
    ├── Installation Phase Monitoring
    ├── Post-installation Execution Monitoring
    │
    ▼
eBPF-based Trace Collection
    │
    ├── Filetop
    ├── Opensnoop
    ├── Install
    ├── TCP
    ├── SysCall
    └── Pattern
    │
    ▼
Behavioral Feature Construction
    │
    ├── Numeric normalization
    ├── Categorical/pattern TF-IDF encoding
    └── Sequence-style serialization for sequence models
    │
    ▼
Feature Selection
    │
    ├── ANOVA
    ├── CORR
    ├── FLAML
    ├── PSO
    └── WOA
    │
    ▼
Deep Learning Model Evaluation
    │
    ├── Classical: CNN, MLP, LeNet, MDCNN, NN
    ├── Pre-attention: LSTM, RNN
    └── Attention: Transformer, BERT, DistilGPT2
    │
    ▼
Prediction + XAI + Stability Analysis
```

### Architecture Animation

<p align="center">
  <img src="docs/animations/edysec-architecture.gif" alt="eDySec architecture animation" width="85%">
</p>

<p align="center">
  <em>Recommended GIF idea: animate data flow from package execution to traced events, selected features, model prediction, and explanation dashboard.</em>
</p>

---

## Dataset

eDySec is designed around **QUT-DV25**, a dynamic behavioral dataset built to capture runtime traces from Python packages during both installation and post-installation execution.

The dataset supports analysis of:

* benign packages,
* malicious packages,
* heterogeneous runtime behaviors,
* sparse and high-dimensional dynamic features, and
* trace-specific as well as combined behavioral representations.

### Data Split

A typical experimental setup uses:

* **70%** training
* **15%** validation
* **15%** testing

This enables fair model selection, validation-driven optimization, and final holdout evaluation.

---

## Trace Categories

eDySec analyzes six core trace categories, plus a combined representation:

| Trace Type    | Description                                                           |
| ------------- | --------------------------------------------------------------------- |
| **Filetop**   | File activity summaries and file interaction behavior                 |
| **Opensnoop** | File open operations and related access patterns                      |
| **Install**   | Installation-phase activity and package setup behavior                |
| **TCP**       | Network communication behavior                                        |
| **SysCall**   | System call-level runtime interactions                                |
| **Pattern**   | Behavioral pattern representations extracted from execution artifacts |
| **Combined**  | Joint representation built from all trace categories                  |

### Observed Insights

* **Combined traces** provide the strongest overall detection performance.
* **Filetop** and **SysCall** are among the most informative individual trace sources.
* **Install** traces can offer useful signals, but when used alone may exhibit relatively high false positive behavior.
* **TCP** and **Opensnoop** provide complementary runtime evidence.

---

## Methodology

## 1. Data Preparation

Behavioral traces are transformed into model-ready representations using a structured preprocessing pipeline.

### Numerical Features

Numerical features are standardized using **z-score normalization**, with statistics computed from the training partition and applied consistently to validation and test sets.

### Categorical and Pattern Features

Categorical and pattern-oriented features are transformed using **TF-IDF encoding**, typically with **bigram** and **trigram** vocabularies learned from the training data.

### Sequence-Oriented Inputs

For sequence-based architectures, features can be serialized into **feature-value token sequences**, allowing models such as LSTM, RNN, and Transformer-based architectures to ingest structured behavioral information in sequential form.

---

## 2. Feature Selection

Dynamic behavioral datasets are often high-dimensional, sparse, heterogeneous, and noisy. To address this, eDySec evaluates a portfolio of complementary feature selection strategies:

* **ANOVA**: selects features based on discriminative statistical ranking.
* **CORR**: prioritizes features strongly associated with the target while reducing redundancy.
* **FLAML**: uses data-driven importance estimates to identify compact predictive subsets.
* **PSO**: applies population-based probabilistic search for feature subset optimization.
* **WOA**: explores feature subsets using whale optimization-inspired search dynamics.

The goal is to balance:

* predictive performance,
* dimensionality reduction,
* generalization ability, and
* downstream interpretability.

---

## 3. Deep Learning Model Evaluation

eDySec evaluates **nine deep learning models** across three families.

### Classical Deep Learning

* CNN
* MLP
* LeNet
* MDCNN
* NN

### Pre-Attention Models

* LSTM
* RNN

### Attention-Based Models

* Transformer
* BERT
* DistilGPT2

### Key Observation

Across compact, behaviorally discriminative feature subsets, **lightweight classical deep learning models** consistently perform strongly, with **MLP** emerging as the best overall model in the most effective configuration.

---

## 4. Stability and Explainability

### Stability Analysis

eDySec goes beyond single-run accuracy reporting by analyzing model stability using:

* mean performance across runs,
* standard deviation,
* confidence intervals,
* average ranking, and
* comparative robustness assessment.

### Explainability

To improve trust and interpretability, eDySec integrates:

* **SHAP** for local and global feature attribution, and
* **LIME** for local, instance-level explanations.

This helps verify whether the model is learning **security-relevant behavioral evidence** rather than relying on accidental correlations.

<p align="center">
  <img src="docs/images/shap-summary.png" alt="SHAP summary plot" width="80%">
</p>

<p align="center">
  <img src="docs/animations/lime-local-explanation.gif" alt="LIME local explanation animation" width="80%">
</p>

<p align="center">
  <em>Suggested assets: one SHAP summary plot and one animated walkthrough of a local LIME explanation for a malicious package prediction.</em>
</p>

---

## Performance Summary

### Main Outcome

The best eDySec configuration uses:

* **Combined traces**
* **FLAML-based feature selection**
* **MLP classifier**

### Reported Highlights

* Achieves approximately **0.99 accuracy** and **0.99 F1-score**.
* Reduces feature dimensionality from **36 to 17 features**.
* Delivers a **52.78% reduction** in feature count.
* Reduces false positives by **67.65%** compared with the DySec baseline.
* Reduces false negatives by **94.23%** compared with the DySec baseline.
* Maintains a low inference latency of approximately **170 ms** after feature extraction.
* Demonstrates **near-perfect stability**, with top-performing models reaching approximately **0.996** on a 0–1 scale.

### Baseline Comparison

| Method             | Feature Count | Accuracy | Key Observation                                                 |
| ------------------ | ------------: | -------: | --------------------------------------------------------------- |
| **DySec baseline** |            36 |  ~95.99% | Strong baseline, but higher false positives and false negatives |
| **eDySec (best)**  |            17 |     ~99% | Higher accuracy, fewer errors, more compact feature space       |

### Performance Visualization

<p align="center">
  <img src="docs/images/performance-comparison.png" alt="Performance comparison" width="90%">
</p>

<p align="center">
  <img src="docs/animations/training-curves.gif" alt="Training curves animation" width="85%">
</p>

<p align="center">
  <em>Suggested visuals: bar chart comparing models and a GIF showing training/validation learning curves across epochs.</em>
</p>

---

## Project Structure

```bash
eDySec/
├── README.md
├── requirements.txt
├── environment.yml
├── data/
│   ├── raw/
│   ├── processed/
│   └── splits/
├── traces/
│   ├── filetop/
│   ├── opensnoop/
│   ├── install/
│   ├── tcp/
│   ├── syscall/
│   └── pattern/
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   ├── 02_feature_selection.ipynb
│   ├── 03_model_training.ipynb
│   ├── 04_evaluation.ipynb
│   └── 05_explainability.ipynb
├── src/
│   ├── preprocessing/
│   ├── feature_selection/
│   ├── models/
│   ├── evaluation/
│   ├── xai/
│   └── utils/
├── outputs/
│   ├── models/
│   ├── logs/
│   ├── figures/
│   ├── shap/
│   └── lime/
├── docs/
│   ├── images/
│   └── animations/
└── LICENSE
```

> Adapt this structure to match your actual repository layout.

---

## Installation

### Option 1: Using `pip`

```bash
git clone https://github.com/your-username/eDySec.git
cd eDySec
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Option 2: Using Conda

```bash
conda create -n edysec python=3.10 -y
conda activate edysec
pip install -r requirements.txt
```

### Typical Core Dependencies

```txt
pandas==1.5.3
scikit-learn==1.2.2
numpy==1.23.5
scipy==1.9.3
tensorflow==2.11.0
matplotlib==3.7.1
seaborn==0.12.2
joblib==1.3.2
shap==0.41.0
flaml==2.5.0
notebook==6.5.6
transformers==4.49.0
```

> Adjust versions to match your validated environment.

---

## Usage

### 1. Prepare Data

```bash
python src/preprocessing/prepare_data.py
```

### 2. Run Feature Selection

```bash
python src/feature_selection/run_feature_selection.py --method flaml
```

### 3. Train a Model

```bash
python src/models/train_mlp.py --features combined_flaml
```

### 4. Evaluate on the Test Set

```bash
python src/evaluation/evaluate.py --model outputs/models/combined_flaml_mlp.h5
```

### 5. Generate Explainability Reports

```bash
python src/xai/run_shap.py
python src/xai/run_lime.py
```

---

## Outputs

The framework can generate the following artifacts:

* trained model checkpoints,
* feature-selected datasets,
* confusion matrices,
* ROC curves,
* learning curves,
* SHAP summary and waterfall plots,
* LIME local explanation reports,
* stability comparison tables, and
* prediction logs for benign and malicious samples.

---

## Explainability

Explainability is a central part of eDySec.

### SHAP

Used to identify:

* globally important behavioral signals,
* feature contribution directionality,
* security-relevant patterns across samples.

### LIME

Used to inspect:

* why an individual package was predicted as malicious or benign,
* which local runtime behaviors contributed to the decision,
* whether the prediction aligns with expected threat indicators.

This makes eDySec more transparent for:

* security researchers,
* malware analysts,
* repository defenders,
* reviewers, and
* operators seeking interpretable package risk assessment.

---

## Reproducibility

To encourage reproducible experimentation:

* keep train/validation/test splits fixed,
* fit preprocessing artifacts only on training data,
* record random seeds,
* report both aggregate and per-run results,
* preserve selected feature subsets,
* version all datasets, scripts, and configurations, and
* archive figures and logs used in papers.

---

## Limitations

While eDySec demonstrates strong promise, several limitations remain:

* The current framework is primarily **Linux-centric** due to eBPF-based tracing.
* Environment-sensitive attacks may behave differently across operating systems, hardware, or runtime contexts.
* Some malicious behaviors may activate only under specific triggers, timing conditions, or user interactions.
* Child-process monitoring and certain evasive behaviors may reduce full visibility in some cases.
* The framework is currently focused on **PyPI**, and direct transfer to other ecosystems may require adaptation or retraining.

---

## Roadmap

Planned future directions include:

* extending platform support to **Windows** and **macOS**,
* improving visibility for multi-process and evasive behaviors,
* expanding to other package ecosystems such as **npm**, **Maven**, and **RubyGems**,
* integrating richer temporal behavioral modeling,
* supporting online or streaming analysis pipelines,
* enhancing XAI dashboards for analyst-friendly investigation, and
* exploring kernel-level behavioral monitoring for AI-agent security scenarios.

---

## Citation

If you use eDySec in your research, please cite the corresponding paper.

```bibtex
@article{mehedi2026edysec,
  title   = {eDySec: A Deep Learning-based Explainable Dynamic Analysis for Detecting Malicious Packages in the PyPI Ecosystem},
  author  = {Mehedi, Sk. Tanzir and others},
  journal = {To be added},
  year    = {2026}
}
```

> Update this entry with the final author list, venue, DOI, and publication details.

---

## Acknowledgment

This work is associated with research on dynamic behavioral analysis, feature-efficient deep learning, and explainable security analytics for software supply-chain defense in the PyPI ecosystem.

If relevant, you may also acknowledge:

* your institution,
* funding support,
* collaborators,
* dataset contributors, and
* computational infrastructure.

---

## License

Specify the license for your repository here.

Examples:

* `MIT License`
* `Apache-2.0`
* `GPL-3.0`
* `CC BY-NC 4.0` for research artifacts, if appropriate

---

## Final Notes for GitHub Presentation

To make this README look exceptional on GitHub, add the following assets under `docs/`:

### Recommended Images

* `docs/images/edysec-banner.png`
* `docs/images/edysec-overview.png`
* `docs/images/performance-comparison.png`
* `docs/images/shap-summary.png`

### Recommended Animations

* `docs/animations/edysec_pipeline.gif`
* `docs/animations/edysec-architecture.gif`
* `docs/animations/training-curves.gif`
* `docs/animations/lime-local-explanation.gif`

### Recommended GIF Content Ideas

1. **Pipeline GIF**: show raw runtime traces entering preprocessing, feature selection, classification, and XAI.
2. **Architecture GIF**: animate each module as a layered research pipeline.
3. **Training GIF**: animate validation accuracy and loss over epochs.
4. **LIME GIF**: animate a malicious sample explanation with feature contributions appearing step by step.

---

## Contact

For questions, collaboration, or research discussion, please open an issue or contact the repository maintainer.

---

<div align="center">

**eDySec brings dynamic behavior, explainable deep learning, and feature-efficient security analysis together for next-generation malicious package detection.**

</div>
