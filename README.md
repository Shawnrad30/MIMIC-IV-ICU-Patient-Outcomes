ICU Capstone (MIMIC-IV Demo) — End-to-End Analytics (Updated Nov 2025)

This repository contains the complete workflow for the MDS Capstone Project on ICU patient-outcomes analytics using the MIMIC-IV demo dataset. The project implements a full CRISP-DM pipeline - from exploratory data analysis through model evaluation and simulated deployment - to support operational and clinical decision-making at Regional Medical Center (RMC). The analysis focuses on improving ICU performance through reductions in length of stay (LOS), in-hospital mortality, and readmission risk, while identifying patient subgroups with different utilization patterns.

Repository structure:
ICU_CAPSTONE/
├─ data/
│  ├─ flat_csv/                                # optional: flattened tables for faster loading
│  ├─ hosp/                                    # MIMIC-IV hosp-level CSVs
│  ├─ icu/                                     # MIMIC-IV ICU-level CSVs
│  └─ demo_subject_id.csv
├─ notebooks/
│  ├─ analytic_admissions_dataset.csv        # final analytic dataset
│  ├─ ICU_EDA.ipynb                          # exploratory analysis
│  ├─ ICU_Data_Preparation.ipynb             # cleaning, feature engineering, integration
│  ├─ ICU_Modeling.ipynb                     # regression, classification, clustering
│  ├─ ICU_Evaluation_&_Deployment.ipynb      # extended evaluation & deployment workflow
│  ├─ kmeans_clusters.pkl                    # saved clustering pipeline
│  ├─ los_random_forest.pkl                  # saved LOS Random Forest model
│  ├─ mortality_logreg.pkl                   # saved mortality model (training version)
│  └─ mortality_logreg_deployment.pkl        # deployment-ready model
├─ consolidate_shards.py                     # utility for merging MIMIC shards
├─ main.py                                   # optional script entry point
├─ pyproject.toml                            # dependencies and project metadata
├─ README.md
├─ .gitignore
├─ .python-version
└─ uv.lock                                   # local environment files

What’s Included:
1. Exploratory Data Analysis (EDA)
   - Patient demographics, admission and discharge patterns
   - ICU LOS distribution, outlier detection, and temporal trends
   - Completeness and accuracy checks (uniqueness, range, timestamp validity)
2. Data Preparation & Feature Engineering
   - Table selection, cleaning, and harmonization across hosp and icu modules
   - Feature creation: LOS (hours/days), transfer counts, readmission flags, etc.
   - Standardization, encoding, and integration into analytic dataset
3. Predictive Modeling
   - Regression (Random Forest): ICU LOS forecasting
   - Classification (Logistic Regression): In-hospital mortality
   - Classification (Random Forest): 30-day readmission
   - Clustering (K-Means): Patient grouping by ICU utilization patterns
4. Evalution and Deployment
   - Extended Model Evaluation
     - Full-dataset predictions
     - Confusion matrix & classification report
     - ROC & precision–recall analysis
     - Calibration curve & Brier score
     - Threshold tuning for risk-stratification scenarios
     - Error profiling and subgroup analysis
     - Coefficient interpretation (odds ratios)
   - Supporting Models
     - LOS model residual analysis, prediction-vs-actual plots
     - Clustering evaluation with silhouette score and PCA visualization
     - Cluster profiling for operational planning

Getting started:
1. Clone & enter
   git clone <repo-url>
   cd ICU_CAPSTONE
2. Create/activate env (choose one)
   Standard Python:
   python -m venv .venv
   # Windows
     .venv\Scripts\activate
   # macOS/Linux
     source .venv/bin/activate
3. Install dependencies
   If using pyproject.toml:
   pip install -e .
4. Add data
   Place the MIMIC-IV demo CSVs in data/hosp/ and data/icu/.
   Optionally subset using demo_subject_id.csv.
5. Run notebooks
   Open with jupyter lab or launch from VS Code under notebooks/.

Typical Workflow:
   - EDA: Summarize population and identify quality issues
   - Data Prep: Clean, engineer, and integrate features across tables
   - Modeling: Train and validate regression/classification/clustering models
   - Evaluation: Assess calibration, discrimination, and error patterns
   - Deployment: Serialize and reuse models; simulate inference scenarios
   - Reporting: Export key figures, metrics, and tables for documentation

Notes & Assumptions:
   - Designed for the MIMIC-IV demo dataset; assumes local CSV access
   - Visualization uses Matplotlib ≥ 3.8 and Seaborn ≥ 0.13
   - Pipelines rely on scikit-learn for preprocessing and modeling
   - All results are for educational and methodological demonstration purposes

Next Steps:
   - Deploy risk scores in a dashboard
   - Incorporate SHAP values for deeper interpretability
   - Integrate temporal models
   - Add real-time inference endpoints

Acknowledgments:
   - Data: MIMIC-IV Demo (MIT Laboratory for Computational Physiology, PhysioNet)
   - License: Use compliant with PhysioNet credentialing and data access requirements