### A Deep Learning-based Explainable Dynamic Analysis Framework for Detecting Malicious Packages in the PyPI Ecosystem

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

<img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python"> <img src="https://img.shields.io/badge/Focus-PyPI%20Malware%20Detection-critical.svg" alt="Focus"> <img src="https://img.shields.io/badge/Analysis-DL%20Based%20Dynamic%20Behavioral-orange.svg" alt="Analysis"> <img src="https://img.shields.io/badge/Stability-Statistical-purple.svg" alt="Stability"> <img src="https://img.shields.io/badge/XAI-SHAP%20%7C%20LIME-purple.svg" alt="XAI">

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## Overview

eDySec is an efficient, stable, and explainable DL-based dynamic analysis framework for detecting malicious packages. It is designed to address the high-dimensional, sparse, and heterogeneous nature of dynamic behavioral data. As illustrated in Figure, eDySec consists of four main phases: 

- Data Preparation    
- Feature Selection    
- Model Selection and Evaluation    
- Stability and Explainability Analysis   

<p align="center">
  <img src="Images/framework.jpg" alt="eDySec Framework" width="60%">
</p>
<p align="center"><b>Figure 1: Proposed eDySec framework for detecting malicious PyPI packages.</b></p>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## Dataset Overview

The experiments were conducted on the **QUT-DV25** dataset, a dynamic behavioral dataset designed for malicious package detection in the **PyPI ecosystem**.

### Dataset Summary

<p align="center">
  <img src="Images/dataset_overview.jpg" alt="Dataset Overview" width="60%">
</p>
<p align="center"><b>Figure 2: Overview of the QUT-DV25 dataset: (a) statistics; (b) class distribution.</b></p>

- **Dataset Name:** QUT-DV25
- **Target Task:** Binary classification of benign and malicious Python packages
- **Ecosystem:** PyPI
- **Total Packages:** 14,271 (7,127 malicious packages)
- **Analysis Type:** Dynamic behavioral analysis
- **Execution Phases:** Install-time and post-installation
- **Trace Categories:** Filetop, Opensnoop, Install, TCP, SysCall, Pattern
- **Feature Representation:** Individual trace-based features and a combined feature space
- **Output Classes:** Benign / Malicious
- **Dataset DOI:** https://doi.org/10.7910/DVN/LBMXJY

### Trace Categories

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

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## Running Prerequisites

Before running the project, ensure that the following requirements are satisfied.

### 1. Experimental Environment

The analysis and experimental evaluation of **eDySec** were conducted in a controlled hardware and software environment. The reported configuration is provided below for reproducibility and reference, and reflects the setup used for model development, training, and evaluation.

#### Hardware and Operating System
- **Processor:** 13th Gen Intel Core i9-13900K
- **Memory:** 128 GB RAM
- **GPU:** NVIDIA RTX A6000 with 48 GB memory
- **Operating System:** Ubuntu 22.04 LTS (64-bit)

#### Python Environment
- **Python Version:** 3.10.20  
- **Compiler:** GCC 14.3.0

#### Core Library Versions
- **NumPy:** 1.23.5
- **Pandas:** 1.5.3
- **Matplotlib:** 3.7.1
- **Seaborn:** 0.12.2
- **SciPy:** 1.9.3
- **Scikit-learn:** 1.2.2
- **TensorFlow:** 2.11.0
- **Transformers:** 4.38.2
- **Joblib:** 1.3.2

#### Deep Learning Backend
- **Keras (`tf.keras`):** 2.11.0

#### GPU Configuration
- **TensorFlow Built with CUDA:** Yes
- **GPU Available:** Yes
- **Detected GPU(s):** `GPU:0`
  
### 2. Running Instructions

### Option 1: pip

```bash
git clone https://github.com/tanzirmehedi/eDySec.git
cd eDySec
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Option 2: conda

```bash
conda create -n edysec python=3.10 -y
conda activate edysec
pip install -r requirements.txt
```

### 3. Required Python Packages

Typical packages used throughout the project include:

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
`pywinpty==2.0.10`  (Only for windows)  `threadpoolctl==3.1.0` (for Ubuntu)   
`terminado==0.17.1`,  
`transformers==4.49.0`.
```
These versions were used to ensure **consistent and reproducible experimental results**.

### 4. Jupyter Notebook

To launch Jupyter Notebook:

```bash
pip install notebook
jupyter notebook
```

### 5. Dataset Availability

The project expects the **QUT-DV25 dataset** and its trace-category folders to be present under:

```bash
Phase (i) Data Preparation/QUT-DV25 Dataset/
```

Make sure the dataset files remain in their original repository structure before running the notebooks.

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## Repository Structure

```json
{
  "eDySec": {
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
    "README.md": null
    "SECURITY.md": null
    "edysec_runner.py": null
    "requirements.txt": null,
  }
}
```

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## How to Run the Project (Individual Script)

The repository follows a four-phase execution workflow. For reproducibility and consistency, run the notebooks in the order below.

<p align="center">
  <img src="Images/motivation.jpg" alt="eDySec banner" width="60%">
</p>
<p align="center"><b>Figure 3: Overall system architecture of the proposed eDySec framework.</b></p>

### Phase 1: Data Preparation

This phase introduces the dataset structure and provides visualization of the underlying data distributions.

Run the following notebooks:

```bash
Phase (i) Data Preparation/Dataset Overview.ipynb    
Phase (i) Data Preparation/t-SNE Implementation.ipynb
```

This phase produces:

* dataset overview outputs
* trace source visualizations
* t-SNE visualizations for dynamic, metadata, and static perspectives

### Phase 2: Feature Selection

This phase applies the feature selection methods used in the study.

Go to:

```bash
Phase (ii) Feature Selection/Feature Selection Methods/
```

The available methods are:

* **ANOVA**
* **CORR**
* **FLAML**
* **PSO**
* **WOA**

For each method, run the notebook corresponding to the required trace category.

Example:

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

### Phase 3: Model Selection and Evaluation

This phase trains and evaluates the deep learning models using the selected feature subsets.

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

Then open the required trace-category folder and run the corresponding notebook.

For example, under `FLAML/Pattern/`:

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

### Phase 4: Stability and Explainability Analysis

This phase performs comparative stability analysis across models and feature-selection methods, and provides explainability analysis for the best-performing configuration.

For **stability analysis**, run:

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

For **explainability analysis**, run:

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

### Recommended End-to-End Execution Order

For a full reproduction of the project workflow, run the repository in the following order:

1. `Dataset Overview.ipynb`
2. `t-SNE Implementation.ipynb`
3. feature selection notebooks for the chosen method(s)
4. deep learning evaluation notebooks for the selected features
5. `FLAML DL MLP Combined XAI.ipynb`
6. `Stability Analysis.ipynb`

---

### Core Outputs

The repository generates the following outputs:

* dataset overview figures
* trace source figures
* t-SNE visualizations
* selected feature summaries
* confusion matrices
* ROC curves
* learning curves
* evaluation summary files
* training logs
* SHAP explanations
* LIME dashboards and local explanations
* stability analysis figures and statistical reports

---

### Best Reported Configuration

The strongest reported configuration in this repository is:

* **Combined traces**
* **FLAML feature selection**
* **MLP model**

This configuration is also used in the explainability phase.

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## How to Run the Project in GitHub Dev Environment or Local PC (using edysec_runner.py)

This repository includes `edysec_runner.py`, a Python utility to help you **check the project structure**, **set up the environment**, and **run all Jupyter notebooks (`.ipynb`)** across folders and subfolders in the correct order.

To run this project in **GitHub Codespaces / GitHub Dev**, open the repository in GitHub Dev by replacing `.com` with `.dev` in the URL: https://github.dev/tanzirmehedi/eDySec/

Once the environment is opened, launch the terminal and run the required setup and execution commands provided in the project.

###  Important Note
Before executing the pipeline, please ensure that all **dataset paths and locations** are correctly configured according to your environment. Incorrect dataset paths may result in runtime errors or missing data issues.

---

### What the Runner Does

The script supports the following tasks:

- validates the repository structure
- checks that key folders and files exist
- installs dependencies from `requirements.txt`
- discovers notebooks recursively inside subfolders
- runs notebooks in the expected workflow order
- executes each notebook from its own directory so relative paths continue to work
- optionally saves executed notebooks to a separate output directory
- writes an execution summary report
- can continue even if some notebooks fail

---

### Main Commands (Ubuntu)

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
cd /workspaces/eDySec
pyenv local 3.10.20
python --version   # should show Python 3.10.20
```

#### 5. Create virtual environment

```bash
python -m venv eDySec
```
Activate it:

```bash
source /workspaces/eDySec/eDySec/bin/activate
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
python edysec_runner.py check
```

#### 8. Set up the environment

This installs the required Python packages from `requirements.txt`.

```bash
python edysec_runner.py setup
```

#### 9. Run the full workflow

Run only Phase 2

```bash
python edysec_runner.py run --phase 2
```

This runs all notebooks across all phases.

```bash
python edysec_runner.py run --phase all --continue-on-error
```

---

### Useful Examples

#### Only list what will run

This performs a dry run without executing notebooks.

```bash
python edysec_runner.py run --dry-run
```

#### Run only specific script within a Phase

```bash
python edysec_runner.py run --phase 2 --method PSO --trace SysCall
```

#### Run only FLAML notebooks

```bash
python edysec_runner.py run --phase all --method FLAML
```

#### Run only FLAML Pattern notebooks

```bash
python edysec_runner.py run --phase 3 --method FLAML --trace Pattern
```

#### Run only FLAML SysCall CNN notebooks

```bash
python edysec_runner.py run --phase 3 --method FLAML --trace SysCall "SysCall_FLAML_CNN.ipynb"
```

#### Overwrite the original notebooks

By default, executed notebooks are saved separately. If you want to overwrite the original notebooks instead, use:

```bash
python edysec_runner.py run --in-place --continue-on-error
```

---

### Default Outputs

By default, the script saves executed notebooks into:

```text
executed_notebooks/
```

It also writes an execution summary file:

```text
execution_summary.json
```

---

### Recommended Execution Order

For a complete end-to-end workflow, run the commands in this order:

```bash
python edysec_runner.py check
python edysec_runner.py setup
python edysec_runner.py run --phase all --continue-on-error
```

---

### Phase-Based Execution

If your project follows a multi-phase workflow, you can run specific phases only.

Example:

```bash
python edysec_runner.py run --phase 1
python edysec_runner.py run --phase 2
python edysec_runner.py run --phase 3
python edysec_runner.py run --phase 4
```

You can also combine phase selection with method and trace filtering.

Example:

```bash
python edysec_runner.py run --phase 3 --method FLAML --trace Pattern
```

---

### Notes

- The script executes each notebook from its **own folder**.
- This is important for notebooks that use **relative paths**.
- The script is suitable for projects with **folders and subfolders**.
- It is especially useful when notebooks depend on a fixed repository layout.

---

### Expected Dataset Location

If your notebooks rely on the dataset being stored in a specific location, keep the dataset in the original repository structure.

For example, in the eDySec layout the dataset is expected under:

```text
Phase (i) Data Preparation/QUT-DV25 Dataset/
```

Do not move dataset files unless you also update the notebook paths.

---

### Troubleshooting

#### 1. `requirements.txt` not found
Make sure you are running the script from the repository root.

#### 2. Notebook path errors
This usually happens when dataset folders or relative paths are missing or changed.

#### 3. Some notebooks fail but others should continue
Use:

```bash
python edysec_runner.py run --phase all --continue-on-error
```

#### 4. You only want to preview the execution plan
Use:

```bash
python edysec_runner.py run --dry-run
```

---

### Example Workflow

```bash
# Step 1: validate repository structure
python edysec_runner.py check

# Step 2: install dependencies
python edysec_runner.py setup

# Step 3: preview the notebooks that will run
python edysec_runner.py run --dry-run

# Step 4: execute everything
python edysec_runner.py run --phase all --continue-on-error
```

---

### Output Summary

After execution, check:

- `executed_notebooks/` for executed notebook copies
- `execution_summary.json` for run status and summary information

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## Note on Model Naming Consistency

In this repository and the accompanying paper, the correct model name is MDCNN (Multi-Dimensional Convolutional Neural Network).
Due to a typographical inconsistency, the name MCDCNN may appear in parts of the analysis code and intermediate results.

Please note that MCDCNN is a typo and refers to the same MDCNN model used throughout the paper. All results labeled as MCDCNN should be interpreted as MDCNN.

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## Citation

```bibtex
@article{edysec,
  title   = {eDySec: A Deep Learning-based Explainable Dynamic Analysis Framework for Detecting Malicious Packages in the PyPI Ecosystem},
  author  = {Will be added},
  year    = {will be added}
}
```
<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## License

This project is distributed under the terms specified in the `LICENSE` file.
