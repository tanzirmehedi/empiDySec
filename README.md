# An Empirical Study of Deep Learning for Dynamic Behavioral Detection of Malicious Software Packages

**Replication Package - empiDySec (Empirical Dynamic Security)**

---

<img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python"> <img src="https://img.shields.io/badge/Focus-PyPI%20Malware%20Detection-critical.svg" alt="Focus"> <img src="https://img.shields.io/badge/Analysis-DL%20Based%20Dynamic%20Behavioral-orange.svg" alt="Analysis"> <img src="https://img.shields.io/badge/Stability-Statistical-purple.svg" alt="Stability"> <img src="https://img.shields.io/badge/XAI-SHAP%20%7C%20LIME-purple.svg" alt="XAI">

---

## 1. Study Overview

This repository contains the complete replication package for our empirical study on deep learning (DL)-based **dynamic behavioral detection of malicious software packages** in the PyPI ecosystem. The study systematically investigates how feature selection strategies, DL architectures, trace categories, model stability, and explainability interact when detecting malicious packages from high-dimensional, sparse, and heterogeneous dynamic behavioral data.

The study is operationalized through **empiDySec** - an efficient, stable, and explainable DL-based empirical dynamic analysis approach evaluated on the **QUT-DV25** dataset. As illustrated in Figure 1, the empirical study is structured into four sequential phases:

1. **Data Preparation** - dataset characterization and visualization
2. **Feature Selection** - comparative evaluation of five selection strategies
3. **Model Selection and Evaluation** - benchmarking of ten DL architectures
4. **Stability and Explainability Analysis** - statistical robustness testing and XAI interpretation

<p align="center">
  <img src="Images/framework.jpg" alt="empiDySec Study Workflow" width="60%">
</p>
<p align="center"><b>Figure 1: Workflow of the empiDySec empirical study for detecting malicious PyPI packages.</b></p>

---

## 2. Research Questions

The empirical study is designed around the following research questions:

    - RQ1: Which feature sets lead to the best performance?
    - RQ2: How do DL models compare to ML models?
    - RQ3: Can DL models detect evasive attacks?
    - RQ4: How do DL models ensure stability?
    - RQ5: Can XAI provide meaningful interpretations? 

---

## 3. Subject Dataset: QUT-DV25

All experiments were conducted on **QUT-DV25**, a dynamic behavioral dataset constructed for malicious package detection in the **PyPI ecosystem**.

<p align="center">
  <img src="Images/dataset_overview.jpg" alt="Dataset Overview" width="60%">
</p>
<p align="center"><b>Figure 2: Overview of the QUT-DV25 dataset: (a) statistics; (b) class distribution.</b></p>

| Property | Value |
| --- | --- |
| **Dataset name** | QUT-DV25 |
| **Target task** | Binary classification (benign vs. malicious Python packages) |
| **Ecosystem** | PyPI |
| **Total packages** | 14,271 (7,127 malicious) |
| **Analysis type** | Dynamic behavioral analysis |
| **Execution phases** | Install-time and post-installation |
| **Trace categories** | Filetop, Opensnoop, Install, TCP, SysCall, Pattern |
| **Feature representation** | Individual trace-based features and a combined feature space |
| **Output classes** | Benign / Malicious |
| **Dataset DOI** | https://doi.org/10.7910/DVN/LBMXJY |

### 3.1 Trace Categories (Independent Variables)

The study analyzes six core trace categories, plus a combined representation:

| Trace Type | Description |
| --- | --- |
| **Filetop** | File activity summaries and file interaction behavior |
| **Opensnoop** | File open operations and related access patterns |
| **Install** | Installation-phase activity and package setup behavior |
| **TCP** | Network communication behavior |
| **SysCall** | System call-level runtime interactions |
| **Pattern** | Behavioral pattern representations extracted from execution artifacts |
| **Combined** | Joint representation built from all trace categories |

---

## 4. Study Design

### 4.1 Experimental Factors

The empirical evaluation forms a full factorial design over three factors:

- **Feature selection method (5 levels):** ANOVA, CORR, FLAML, PSO, WOA
- **Trace category (7 levels):** Filetop, Opensnoop, Install, TCP, SysCall, Pattern, Combined
- **DL architecture (10 levels):** MLP, NN, CNN, LeNet, MDCNN, RNN, LSTM, Transformer, BERT, DistilGPT2

This yields the full experimental grid executed in Phase (iii), with each configuration producing confusion matrices, ROC curves, learning curves, evaluation summaries, and training logs.

### 4.2 Evaluation and Statistical Analysis

- **Phase (i)** characterizes the dataset (class distribution, trace sources) and visualizes class separability using **t-SNE** across dynamic, metadata, and static views.
- **Phase (ii)** produces per-method, per-trace feature subsets, consolidated in per-trace result workbooks.
- **Phase (iii)** trains and evaluates each DL architecture on each selected feature subset.
- **Phase (iv)** performs comparative **stability analysis** (mean–std–rank summaries, performance heatmaps, category-wise comparisons, **Friedman and Nemenyi critical difference diagrams**, and p-value matrices) and **explainability analysis** of the best configuration using **SHAP** (global importance, summary, and waterfall plots) and **LIME** (dashboards and instance-level local explanations).

---

## 5. Experimental Environment

For GitHub Codespaces (Dev environment), the default configuration is sufficient to reproduce outputs, though performance may vary or degrade relative to the local setup below due to limited hardware resources. The following controlled environment was used for full-scale model development, training, and evaluation, and is reported for reproducibility.

### 5.1 Hardware and Operating System

- **Processor:** 13th Gen Intel Core i9-13900K
- **Memory:** 128 GB RAM
- **GPU:** NVIDIA RTX A6000 with 48 GB memory
- **Operating System:** Ubuntu 22.04 LTS (64-bit)

### 5.2 Python Environment

- **Python Version:** 3.10.20
- **Compiler:** GCC 14.3.0

### 5.3 Core Library Versions

- **NumPy:** 1.23.5
- **Pandas:** 1.5.3
- **Matplotlib:** 3.7.1
- **scikit-posthocs:** 0.12.0
- **Seaborn:** 0.12.2
- **SciPy:** 1.9.3
- **Scikit-learn:** 1.2.2
- **TensorFlow:** 2.11.0
- **Transformers:** 4.38.2
- **Joblib:** 1.3.2

### 5.4 Deep Learning Backend

- **Keras (`tf.keras`):** 2.11.0

### 5.5 GPU Configuration

- **TensorFlow Built with CUDA:** Yes
- **GPU Available:** Yes

---

## 6. Repository Structure

The repository mirrors the four study phases:

```json
{
  "empiDySec": {
    "Phase (i) Data Preparation": {
      "QUT-DV25 Dataset": {
        "QUT-DV25_Filetop_Traces": {},
        "QUT-DV25_Install_Traces": {},
        "QUT-DV25_Opensnoop_Traces": {},
        "QUT-DV25_Pattern_Traces": {},
        "QUT-DV25_SysCall_Traces": {},
        "QUT-DV25_TCP_Traces": {}
      },
      "Dataset Overview.ipynb": null,
      "dataset_overview.png": null,
      "qutdv25_trace_sources.png": null,
      "t-SNE Implementation.ipynb": null,
      "tsne_Dynamic.png": null,
      "tsne_Metadata.png": null,
      "tsne_Static.png": null
    },
    "Phase (ii) Feature Selection": {
      "Feature Selection Methods": {
        "ANOVA": {
          "Feature_Selection_Combined_ANOVA.ipynb": null,
          "Feature_Selection_Filetop_ANOVA.ipynb": null,
          "Feature_Selection_Install_ANOVA.ipynb": null,
          "Feature_Selection_Opensnoop_ANOVA.ipynb": null,
          "Feature_Selection_Pattern_ANOVA.ipynb": null,
          "Feature_Selection_SysCall_ANOVA.ipynb": null,
          "Feature_Selection_TCP_ANOVA.ipynb": null
        },
        "CORR": "...",
        "FLAML": "...",
        "PSO": "...",
        "WOA": "..."
      },
      "Feature Selection Result": {
        "Combined.xlsx": null,
        "Filetop.xlsx": null,
        "Install.xlsx": null,
        "Opensnoop.xlsx": null,
        "Pattern.xlsx": null,
        "SysCall.xlsx": null,
        "TCP.xlsx": null
      },
      "Feature Selection Overview.csv": null,
      "Features Selection Overview.ipynb": null,
      "feature_selection.png": null,
      "six_feature_selection.png": null
    },
    "Phase (iii) DL Model Selection & Evaluation": {
      "ANOVA": "...",
      "CORR": "...",
      "FLAML": {
        "Combined": "...",
        "Filetop": "...",
        "Install": "...",
        "Opensnoop": "...",
        "Pattern": {
          "Evaluation_Outputs_Pattern_FLAML_Attention_BERT": {},
          "Evaluation_Outputs_Pattern_FLAML_Attention_DistilGPT2": {},
          "Evaluation_Outputs_Pattern_FLAML_Attention_Transformer": {},
          "Evaluation_Outputs_Pattern_FLAML_Classical_CNN": {},
          "Evaluation_Outputs_Pattern_FLAML_Classical_LeNet": {},
          "Evaluation_Outputs_Pattern_FLAML_Classical_MDCNN": {},
          "Evaluation_Outputs_Pattern_FLAML_Classical_MLP": {},
          "Evaluation_Outputs_Pattern_FLAML_Classical_NN": {},
          "Evaluation_Outputs_Pattern_FLAML_Pre_Attention_LSTM": {},
          "Evaluation_Outputs_Pattern_FLAML_Pre_Attention_RNN": {},
          "Pattern_FLAML_BERT.ipynb": null,
          "Pattern_FLAML_CNN.ipynb": null,
          "Pattern_FLAML_DistilGPT2.ipynb": null,
          "Pattern_FLAML_LeNet.ipynb": null,
          "Pattern_FLAML_LSTM.ipynb": null,
          "Pattern_FLAML_MDCNN.ipynb": null,
          "Pattern_FLAML_MLP.ipynb": null,
          "Pattern_FLAML_NN.ipynb": null,
          "Pattern_FLAML_RNN.ipynb": null,
          "Pattern_FLAML_Transformer.ipynb": null
        },
        "SysCall": "...",
        "TCP": "..."
      },
      "PSO": "...",
      "WOA": "..."
    },
    "Phase (iv) Stability & Explainability": {
      "Explainability Analysis": {
        "LIME Outputs": {},
        "SHAP Outputs": {},
        "FLAML DL MLP Combined XAI.ipynb": null
      },
      "Stability Analysis": {
        "Stability Analysis Outputs": {},
        "Stability Analysis.ipynb": null
      }
    },
    "Related Works": {},
    "Images": {},
    "LICENSE": null,
    "README.md": null,
    "SECURITY.md": null,
    "empidysec_runner.py": null,
    "requirements.txt": null
  }
}
```

---

## 7. Reproducing the Study in GitHub Dev Env

This repository includes `empidysec_runner.py`, a Python utility to **check the project structure**, **set up the environment**, and **run all Jupyter notebooks (`.ipynb`)** across folders and subfolders in the correct study order.

To run this project in **GitHub Codespaces / GitHub Dev**, open the repository in GitHub Dev by replacing `.com` with `.dev` in the URL: https://github.dev/****/empiDySec/

Once the environment is opened, launch the terminal and run the required setup and execution commands provided below.

### Important Note

Before executing the pipeline, please ensure that all **dataset paths and locations** are correctly configured according to your environment. Incorrect dataset paths may result in runtime errors or missing data issues.

### 7.1 What the Runner Does

- validates the repository structure
- checks that key folders and files exist
- installs dependencies from `requirements.txt`
- discovers notebooks recursively inside subfolders
- runs notebooks in the expected study workflow order
- executes each notebook from its own directory so relative paths continue to work
- optionally saves executed notebooks to a separate output directory
- writes an execution summary report
- can continue even if some notebooks fail

### 7.2 Main Commands (Ubuntu)

#### 1. Install system dependencies

```bash
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl git \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
libffi-dev liblzma-dev
```

#### 2. Install pyenv

```bash
curl https://pyenv.run | bash
```

Add pyenv to your shell:

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc
```

Apply changes:

```bash
source ~/.bashrc
```

#### 3. Install Python 3.10.20

```bash
pyenv install 3.10.20
```

#### 4. Set project Python version

```bash
cd /workspaces/empiDySec
pyenv local 3.10.20
python --version   # should show Python 3.10.20
```

#### 5. Create virtual environment

```bash
python -m venv empiDySec
```

Activate it:

```bash
source /workspaces/empiDySec/empiDySec/bin/activate
```

Verify:

```bash
python --version
```

#### 6. Install required Python packages

```bash
python -m pip install --upgrade pip
python -m pip install nbformat nbclient jupyter ipykernel
```

#### 7. Check the repository structure

Use this first to verify that the expected folders and files are present.

```bash
python empidysec_runner.py check
```

#### 8. Set up the environment

This installs the required Python packages from `requirements.txt`.

```bash
python empidysec_runner.py setup
```

#### 9. Only list what will run

This performs a dry run without executing notebooks.

```bash
python empidysec_runner.py run --dry-run
```

#### 10. Run only a specific script within Phase 2

```bash
python empidysec_runner.py run --phase 2 --method PSO --trace SysCall
```

#### 11. Run the full study workflow (387 notebooks)

Run only Phase 2:

```bash
python empidysec_runner.py run --phase 2
```

Run all notebooks across all phases:

```bash
python empidysec_runner.py run --phase all --continue-on-error
```

### 7.3 Useful Examples

Run only FLAML notebooks:

```bash
python empidysec_runner.py run --phase all --method FLAML
```

Run only FLAML Pattern notebooks:

```bash
python empidysec_runner.py run --phase 3 --method FLAML --trace Pattern
```

Run only the FLAML SysCall CNN notebook:

```bash
python empidysec_runner.py run --phase 3 --method FLAML --trace SysCall "SysCall_FLAML_CNN.ipynb"
```

Overwrite the original notebooks (by default, executed notebooks are saved separately):

```bash
python empidysec_runner.py run --in-place --continue-on-error
```

### 7.4 Default Outputs

By default, the script saves executed notebooks into:

```text
executed_notebooks/
```

It also writes an execution summary file:

```text
execution_summary.json
```

### 7.5 Recommended Execution Order

For a complete end-to-end reproduction of the study, run the commands in this order:

```bash
python empidysec_runner.py check
python empidysec_runner.py setup
python empidysec_runner.py run --phase all --continue-on-error
```

### 7.6 Phase-Based Execution

Since the study follows a multi-phase design, individual phases can be reproduced independently:

```bash
python empidysec_runner.py run --phase 1
python empidysec_runner.py run --phase 2
python empidysec_runner.py run --phase 3
python empidysec_runner.py run --phase 4
```

Phase selection can also be combined with method and trace filtering:

```bash
python empidysec_runner.py run --phase 3 --method FLAML --trace Pattern
```

### 7.7 Notes

- The script executes each notebook from its **own folder**.
- This is important for notebooks that use **relative paths**.
- The script is suitable for projects with **folders and subfolders**.
- It is especially useful when notebooks depend on a fixed repository layout.

### 7.8 Expected Dataset Location

The notebooks rely on the dataset being stored in its original repository location:

```text
Phase (i) Data Preparation/QUT-DV25 Dataset/
```

Do not move dataset files unless you also update the notebook paths.

### 7.9 Troubleshooting

1. **`requirements.txt` not found** - make sure you are running the script from the repository root.
2. **Notebook path errors** - this usually happens when dataset folders or relative paths are missing or changed.
3. **Some notebooks fail but others should continue** - use `python empidysec_runner.py run --phase all --continue-on-error`.
4. **You only want to preview the execution plan** - use `python empidysec_runner.py run --dry-run`.

### 7.10 Example Workflow

```bash
# Step 1: validate repository structure
python empidysec_runner.py check

# Step 2: install dependencies
python empidysec_runner.py setup

# Step 3: preview the notebooks that will run
python empidysec_runner.py run --dry-run

# Step 4: execute everything
python empidysec_runner.py run --phase all --continue-on-error
```

### 7.11 Output Summary

After execution, check:

- `executed_notebooks/` for executed notebook copies
- `execution_summary.json` for run status and summary information

---

## 8. Reproducing the Study on a Local PC

### 8.1 Option 1: pip

```bash
git clone https://github.com/****/empiDySec.git
cd empiDySec
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 8.2 Option 2: conda

```bash
conda create -n empidysec python=3.10 -y
conda activate empidysec
pip install -r requirements.txt
```

### 8.3 Required Python Packages

Typical packages used throughout the study include:

```bash
`pandas==1.5.3`,
`scikit-learn==1.2.2`,
`openpyxl`,
`numpy==1.23.5`,
`scipy==1.9.3`,
`tensorflow==2.11.0`,
`matplotlib==3.7.1`,
`seaborn==0.12.2`,
`joblib==1.3.2`,
`shap==0.41.0`,
`lime`,
`flaml[automl]==2.5.0`,
`notebook==6.5.6`,
`pywinpty==2.0.10`  (Only for Windows)  `threadpoolctl==3.1.0` (for Ubuntu)
`terminado==0.17.1`,
`transformers==4.49.0`,
`scikit-posthocs==0.12.0`.
```

These versions were used to ensure **consistent and reproducible experimental results**.

### 8.4 Jupyter Notebook

To launch Jupyter Notebook:

```bash
pip install notebook
jupyter notebook
```

### 8.5 Dataset Availability

The study expects the **QUT-DV25 dataset** and its trace-category folders to be present under:

```bash
Phase (i) Data Preparation/QUT-DV25 Dataset/
```

Make sure the dataset files remain in their original repository structure before running the notebooks.

---

## 9. Phase-by-Phase Reproduction Protocol

The repository follows a four-phase execution workflow. For reproducibility and consistency with the reported results, run the notebooks in the order below.

### Phase 1: Data Preparation (RQ1)

This phase characterizes the dataset structure and visualizes the underlying data distributions.

Run the following notebooks:

```bash
Phase (i) Data Preparation/Dataset Overview.ipynb
Phase (i) Data Preparation/t-SNE Implementation.ipynb
```

This phase produces:

- dataset overview outputs
- trace source visualizations
- t-SNE visualizations for dynamic, metadata, and static perspectives

### Phase 2: Feature Selection (RQ2)

This phase applies the five feature selection methods compared in the study.

Go to:

```bash
Phase (ii) Feature Selection/Feature Selection Methods/
```

The evaluated methods are:

- **ANOVA**
- **CORR**
- **FLAML**
- **PSO**
- **WOA**

For each method, run the notebook corresponding to the required trace category. Example (ANOVA):

```bash
Phase (ii) Feature Selection/Feature Selection Methods/ANOVA/Feature_Selection_Combined_ANOVA.ipynb
Phase (ii) Feature Selection/Feature Selection Methods/ANOVA/Feature_Selection_Filetop_ANOVA.ipynb
Phase (ii) Feature Selection/Feature Selection Methods/ANOVA/Feature_Selection_Install_ANOVA.ipynb
Phase (ii) Feature Selection/Feature Selection Methods/ANOVA/Feature_Selection_Opensnoop_ANOVA.ipynb
Phase (ii) Feature Selection/Feature Selection Methods/ANOVA/Feature_Selection_Pattern_ANOVA.ipynb
Phase (ii) Feature Selection/Feature Selection Methods/ANOVA/Feature_Selection_SysCall_ANOVA.ipynb
Phase (ii) Feature Selection/Feature Selection Methods/ANOVA/Feature_Selection_TCP_ANOVA.ipynb
```

Run the corresponding notebooks in the same way for CORR, FLAML, PSO, and WOA.

The generated and consolidated feature selection outputs are available under:

```bash
Phase (ii) Feature Selection/Feature Selection Result/
```

### Phase 3: Model Selection and Evaluation (RQ3)

This phase trains and evaluates the deep learning models on the selected feature subsets.

Go to:

```bash
Phase (iii) DL Model Selection & Evaluation/
```

Choose the desired feature-selection method directory, such as:

```bash
ANOVA/
CORR/
FLAML/
├── Combined/
├── Filetop/
├── Install/
├── Opensnoop/
├── Pattern/
├── SysCall/
└── TCP/
PSO/
WOA/
```

Then open the required trace-category folder and run the corresponding notebook. For example, under `FLAML/Pattern/`:

```bash
Phase (iii) DL Model Selection & Evaluation/FLAML/Pattern/Pattern_FLAML_BERT.ipynb
Phase (iii) DL Model Selection & Evaluation/FLAML/Pattern/Pattern_FLAML_CNN.ipynb
Phase (iii) DL Model Selection & Evaluation/FLAML/Pattern/Pattern_FLAML_DistilGPT2.ipynb
Phase (iii) DL Model Selection & Evaluation/FLAML/Pattern/Pattern_FLAML_LeNet.ipynb
Phase (iii) DL Model Selection & Evaluation/FLAML/Pattern/Pattern_FLAML_LSTM.ipynb
Phase (iii) DL Model Selection & Evaluation/FLAML/Pattern/Pattern_FLAML_MDCNN.ipynb
Phase (iii) DL Model Selection & Evaluation/FLAML/Pattern/Pattern_FLAML_MLP.ipynb
Phase (iii) DL Model Selection & Evaluation/FLAML/Pattern/Pattern_FLAML_NN.ipynb
Phase (iii) DL Model Selection & Evaluation/FLAML/Pattern/Pattern_FLAML_RNN.ipynb
Phase (iii) DL Model Selection & Evaluation/FLAML/Pattern/Pattern_FLAML_Transformer.ipynb
```

Each notebook generates evaluation outputs inside its corresponding output directory, including:

```text
confusion matrices
ROC curves
learning curves
evaluation summary files
training logs
```

The same procedure should be followed for the other feature-selection methods (`ANOVA`, `CORR`, `PSO`, and `WOA`) by navigating to the corresponding method directory, opening the desired trace-category folder, and running the appropriate notebook following the same naming convention.

### Phase 4: Stability and Explainability Analysis (RQ4–RQ5)

This phase performs comparative stability analysis across models and feature-selection methods, and provides explainability analysis for the best-performing configuration.

For **stability analysis** (RQ4), run:

```bash
Phase (iv) Stability & Explainability/Stability Analysis/Stability Analysis.ipynb
```

This notebook generates outputs in:

```bash
Phase (iv) Stability & Explainability/Stability Analysis/Stability Analysis Outputs/
```

Typical outputs include:

- mean-std-rank summaries
- heatmaps of model performance
- category-wise comparison plots
- critical difference diagrams using Friedman and Nemenyi analysis
- p-value comparison matrices
- compact summaries of best-performing models

For **explainability analysis** (RQ5), run:

```bash
Phase (iv) Stability & Explainability/Explainability Analysis/FLAML DL MLP Combined XAI.ipynb
```

This notebook produces outputs in:

```bash
Phase (iv) Stability & Explainability/Explainability Analysis/LIME Outputs/
Phase (iv) Stability & Explainability/Explainability Analysis/SHAP Outputs/
```

Typical outputs include:

- SHAP global feature importance plots
- SHAP summary plots
- SHAP waterfall plots
- LIME dashboards
- local explanations for benign and malicious samples
- instance-level explanation files in HTML and PNG formats

---

## 10. Recommended End-to-End Execution Order

For a full reproduction of the study, run the repository in the following order:

1. `Dataset Overview.ipynb`
2. `t-SNE Implementation.ipynb`
3. Feature selection notebooks for the chosen method(s)
4. Deep learning evaluation notebooks for the selected features
5. `FLAML DL MLP Combined XAI.ipynb`
6. `Stability Analysis.ipynb`

---

## 11. Study Artifacts and Outputs

Reproducing the study generates the following artifacts:

- dataset overview figures
- trace source figures
- t-SNE visualizations
- selected feature summaries
- confusion matrices
- ROC curves
- learning curves
- evaluation summary files
- training logs
- SHAP explanations
- LIME dashboards and local explanations
- stability analysis figures and statistical reports

---

## 12. Key Finding: Best Reported Configuration

The strongest configuration observed in the empirical study is:

- **Combined traces**
- **FLAML feature selection**
- **MLP model**

This configuration is also the subject of the explainability phase (RQ5).

---

## 13. Threats to Validity and Reproducibility Notes

Due to differences in hardware (e.g., GPU model, CUDA version, CPU architecture, libraries), the script outputs may vary slightly across systems.

Observed variation is typically small (within **0 ~ 1.25** difference at most) and does not affect the overall conclusions of the study.

These differences are expected due to:

- Floating-point precision variations
- Non-deterministic GPU operations
- Backend/library implementation differences

For best reproducibility, please ensure matching:

- Python version
- CUDA/cuDNN versions
- Library dependencies (see `requirements.txt`)

---

## 14. Note on Model Naming Consistency

In this repository and the accompanying paper, the correct model name is **MDCNN** (Multi-Dimensional Convolutional Neural Network). Due to a typographical inconsistency, the name **MCDCNN** may appear in parts of the analysis code and intermediate results.

Please note that MCDCNN is a typo and refers to the same MDCNN model used throughout the study. All results labeled as MCDCNN should be interpreted as MDCNN.

---

## 15. Citation

If you use this replication package, dataset, or results in your research, please cite:

```bibtex
@article{empidysec,
  title   = {An Empirical Study of Deep Learning for Dynamic Behavioral Detection of Malicious Software Packages in the PyPI Ecosystem},
  author  = {Will be added},
  year    = {will be added}
}
```

---

## 16. License

This project is distributed under the terms specified in the `LICENSE` file.
