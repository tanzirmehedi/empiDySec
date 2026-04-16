#### A Deep Learning-based Explainable Dynamic Analysis Framework for Detecting Malicious Packages in the PyPI Ecosystem

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

<img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python"> <img src="https://img.shields.io/badge/Platform-Linux-success.svg" alt="Platform"> <img src="https://img.shields.io/badge/Focus-PyPI%20Malware%20Detection-critical.svg" alt="Focus"> <img src="https://img.shields.io/badge/Analysis-DL%20Based%20Dynamic%20Behavioral-orange.svg" alt="Analysis"> <img src="https://img.shields.io/badge/Stability-Statistical-purple.svg" alt="Stability"> <img src="https://img.shields.io/badge/XAI-SHAP%20%7C%20LIME-purple.svg" alt="XAI"> <img src="https://img.shields.io/badge/Status-Research%20Prototype-informational.svg" alt="Status">

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## Visual Overview

<p align="center">
  <img src="docs/images/edysec-banner.png" alt="eDySec banner" width="100%">
</p>

<p align="center">
  <em>Replace <code>docs/images/edysec-banner.png</code> with your main project banner or graphical abstract.</em>
</p>

## Dataset Overview

[![DOI](https://zenodo.org/badge/DOI/10.7910/DVN/LBMXJY.svg)](https://doi.org/10.7910/DVN/LBMXJY)

## Project Structure

```text
eDySec/
├── Phase (i) Data Preparation/
│   ├── QUT-DV25 Dataset/
│   │   ├── QUT-DV25_Filetop_Traces/
│   │   ├── QUT-DV25_Install_Traces/
│   │   ├── QUT-DV25_Opensnoop_Traces/
│   │   ├── QUT-DV25_Pattern_Traces/
│   │   ├── QUT-DV25_SysCall_Traces/
│   │   └── QUT-DV25_TCP_Traces/
│   ├── Dataset Overview.ipynb
│   ├── dataset_overview.png
│   ├── qutdv25_trace_sources.png
│   ├── t-SNE Implementation.ipynb
│   ├── tsne_Dynamic.png
│   ├── tsne_Metadata.png
│   └── tsne_Static.png
├── Phase (ii) Feature Selection/
│   ├── Feature Selection Methods/
│   │   ├── ANOVA/
│   │   ├── CORR/
│   │   ├── FLAML/
│   │   ├── PSO/
│   │   └── WOA/
│   ├── Feature Selection Result/
│   │   ├── Combined.xlsx
│   │   ├── Filetop.xlsx
│   │   ├── Install.xlsx
│   │   ├── Opensnoop.xlsx
│   │   ├── Pattern.xlsx
│   │   ├── SysCall.xlsx
│   │   └── TCP.xlsx
│   ├── Feature Selection Overview.csv
│   ├── Features Selection Overview.ipynb
│   ├── feature_selection.png
│   └── six_feature_selection.png
├── Phase (iii) DL Model Selection & Evaluation/
│   ├── ANOVA/
│   └── FLAML/
├── Phase (iv) Stability & Explainability/
│   ├── Explainability Analysis/
│   │   ├── LIME Outputs/
│   │   ├── SHAP Outputs/
│   │   └── FLAML DL MLP Combined XAI.ipynb
│   └── Stability Analysis/
│       ├── Stability Analysis Outputs/
│       └── Stability Analysis.ipynb
├── Related Works/
├── LICENSE
└── README.md
```

## Main Components

### Phase (i) Data Preparation

This phase contains the **QUT-DV25** dataset organization, dataset overview notebook, trace source visualization, and t-SNE analysis for dynamic, metadata, and static perspectives.

### Phase (ii) Feature Selection

This phase contains five feature selection methods:

* **ANOVA**
* **CORR**
* **FLAML**
* **PSO**
* **WOA**

It also includes consolidated feature selection result files for each trace category.

### Phase (iii) DL Model Selection & Evaluation

This phase contains model training and evaluation notebooks for different feature selection methods and trace categories. The generated outputs include:

* confusion matrices
* ROC curves
* learning curves
* evaluation summaries
* training logs

### Phase (iv) Stability & Explainability

This phase contains:

* **SHAP outputs** for global and local explanation
* **LIME outputs** for dashboard and instance-level explanation
* **stability analysis outputs** including ranking, statistical comparisons, and critical difference analysis

## Running Instructions

This repository is primarily organized as a **notebook-based research workflow**. The recommended execution order is shown below.

### 1. Data preparation

Open and run:

```text
Phase (i) Data Preparation/Dataset Overview.ipynb
Phase (i) Data Preparation/t-SNE Implementation.ipynb
```

This phase prepares the dataset understanding and visualization for the QUT-DV25 traces.

### 2. Feature selection

Go to:

```text
Phase (ii) Feature Selection/Feature Selection Methods/
```

Then run the notebook for the required method and trace type.

Example:

```text
Phase (ii) Feature Selection/Feature Selection Methods/ANOVA/Feature_Selection_Combined_ANOVA.ipynb
Phase (ii) Feature Selection/Feature Selection Methods/ANOVA/Feature_Selection_Filetop_ANOVA.ipynb
```

Repeat similarly for:

* CORR
* FLAML
* PSO
* WOA

The selected-feature summaries are stored in:

```text
Phase (ii) Feature Selection/Feature Selection Result/
```

### 3. Deep learning model selection and evaluation

Go to:

```text
Phase (iii) DL Model Selection & Evaluation/
```

Choose a feature selection method folder such as:

```text
ANOVA/
FLAML/
```

Then open the target trace-category folder and run the corresponding notebook.

Example:

```text
Phase (iii) DL Model Selection & Evaluation/ANOVA/Combined/Combined_ANOVA_BERT.ipynb
Phase (iii) DL Model Selection & Evaluation/ANOVA/Combined/Combined_ANOVA_LSTM.ipynb
Phase (iii) DL Model Selection & Evaluation/ANOVA/Combined/Combined_ANOVA_RNN.ipynb
Phase (iii) DL Model Selection & Evaluation/ANOVA/Combined/Combined_ANOVA_Transformer.ipynb
Phase (iii) DL Model Selection & Evaluation/ANOVA/Combined/Combined_ANOVA_DistilGPT2.ipynb
```

Each notebook generates outputs inside its corresponding evaluation output directory, including:

* `confusion_matrix_*.png`
* `roc_curve_*.png`
* `learning_curves.png`
* `evaluation_summary.csv`
* `training_log.xlsx`

### 4. Explainability analysis

Open and run:

```text
Phase (iv) Stability & Explainability/Explainability Analysis/FLAML DL MLP Combined XAI.ipynb
```

This generates:

* **LIME Outputs**
* **SHAP Outputs**

Example outputs include:

* SHAP global summary plots
* SHAP waterfall plots
* LIME dashboards
* local explanations for benign and malicious samples

### 5. Stability analysis

Open and run:

```text
Phase (iv) Stability & Explainability/Stability Analysis/Stability Analysis.ipynb
```

This generates:

* mean-std-rank summaries
* model performance heatmaps
* critical difference diagram (Friedman + Nemenyi)
* p-value matrix
* top-performing model-feature combinations
* compact summary figures

## Recommended Workflow

Run the project in this order:

1. **Dataset overview and visualization**
2. **Feature selection**
3. **DL model training and evaluation**
4. **Explainability analysis**
5. **Stability analysis**

## Environment

Use **Python 3.10**.

Typical packages used in this project include:

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

Install dependencies with:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not yet complete, install the required packages manually in your Python 3.10 environment.

## Key Outputs

The repository contains or generates the following research outputs:

* dataset overview figures
* t-SNE visualizations
* selected feature summaries
* confusion matrices
* ROC curves
* learning curves
* evaluation summaries
* training logs
* SHAP plots
* LIME dashboards and local explanations
* stability analysis figures and statistical reports

## Best Reported Configuration

The best reported setup in the project is:

* **Combined traces**
* **FLAML feature selection**
* **MLP model**

It achieves strong detection performance together with explainability and stability analysis.

## Citation

```bibtex
@article{mehedi2026edysec,
  title   = {eDySec: A Deep Learning-based Explainable Dynamic Analysis for Detecting Malicious Packages in the PyPI Ecosystem},
  author  = {Mehedi, Sk. Tanzir and others},
  year    = {2026}
}
```

## License

This project is released under the license provided in the `LICENSE` file.


