
# Bank Marketing Data Preparation Pipeline 

## Overview
This repository contains a professional-grade Data Engineering and Data Science preprocessing pipeline. It is designed to clean, audit, and transform the **Bank Marketing Dataset** (predicting term deposit subscriptions) for future Machine Learning modeling.

## Project Structure
```text
bank_marketing_project/
├── data/
│   ├── raw/                  # Original, immutable datasets
│   └── processed/            # Cleaned data ready for ML
├── docs/                     # Technical reports and documentation
├── notebooks/                # Jupyter notebooks for EDA and experimentation
├── src/                      # Source code for custom transformers and auditing
│   ├── __init__.py
│   ├── audit.py              # Checksum and integrity validation
│   └── transformers.py       # Custom Scikit-Learn pipeline steps
├── main.py                   # Master orchestration script
├── requirements.txt          # Python dependencies
└── README.md                 # Project instructions
```

## Setup Intructions
To replicate this environment locally, follow these steps in your terminal:

### 1. Clone the repository:

```bash
git clone [https://github.com/trigoduoc/bank_marketing_project.git](https://github.com/trigoduoc/bank_marketing_project.git)
cd bank_marketing_project
```
### 2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Execution
To run the automated ETL and preprocessing pipeline:

```bash
python main.py
```