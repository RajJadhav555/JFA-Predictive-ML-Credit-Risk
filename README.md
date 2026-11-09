# JFA-Predictive: Credit Default Prediction & Threshold Optimisation

A machine learning credit risk project built on the [Kaggle "Give Me Some Credit"](https://www.kaggle.com/c/GiveMeSomeCredit) benchmark dataset (150,000 borrowers). This is a self-directed learning project demonstrating end-to-end credit default modelling, feature engineering, profit/loss threshold optimisation, and interactive underwriting via Streamlit.

---

## Key Results

| Metric | Value |
|:---|:---|
| Dataset | 150,000 borrowers (Kaggle benchmark) |
| Best Model | LightGBM (100 trees) |
| AUC-ROC (held-out test set) | **0.8699** on 30,000 unseen borrowers |
| Optimal Probability Cutoff | **0.15** (vs naïve 0.50) |
| Modelled Profit Improvement | +20.7% using $1,500 profit / $10,000 loss assumptions |
| Strongest Default Predictor | `TotalLateEvents` (hand-engineered delinquency sum) |
| Model Explainability | Native TreeSHAP (<1ms marginal feature attribution) |

## What This Project Covers

1. **Data Cleaning & Imputation** — Handled 29,731 missing incomes (median imputation + binary missingness flag), removed age outliers, and Winsorized extreme credit utilisation.
2. **Feature Engineering** — Engineered `TotalLateEvents`, `HasLatePayment`, and `PerCapitaIncome` which became the top 3 predictive features in the final model.
3. **Three-Model Progression** — Logistic Regression (0.8549 AUC) → Random Forest (0.8686 AUC) → LightGBM (0.8699 AUC), each with stratified train/test splits preserving the 6.68% default rate.
4. **Profit/Loss Threshold Optimisation** — Applied unit economics ($1,500 profit per good loan, $10,000 loss per default) to vectorise net profit across all probability cutoffs, identifying 0.15 as optimal.
5. **Enterprise SQL Analytics (MySQL 8.4)** — Bulk-loaded 150k records, added stored generated columns, and built multi-dimensional risk matrices and window functions proving delinquent borrowers generate 67.4% of portfolio loss.
6. **Streamlit Underwriting Cockpit** — Interactive dashboard with `@st.cache_resource` for sub-millisecond inference, executive profit/loss scoreboard, and live applicant risk assessment.
7. **Regulatory Model Explainability (TreeSHAP)** — Integrated sub-millisecond local feature attribution compliant with CCCFA (NZ) and RBNZ Responsible Lending Code, isolating top adverse action risk escalators and mitigating credit strengths.

## Project Structure

```
├── data/
│   ├── credit_data.csv              # Raw Kaggle dataset
│   ├── credit_data_cleaned.csv      # After imputation & outlier handling
│   └── credit_data_engineered.csv   # With engineered features
├── data_audit.py                    # Day 1: Initial data profiling
├── data_cleaning.py                 # Day 2: Imputation & outlier treatment
├── feature_engineering.py           # Day 3: Feature creation
├── baseline_model.py               # Day 4: Logistic Regression benchmark
├── feature_importance.py            # Day 5: Odds Ratios & risk multipliers
├── tree_model.py                    # Day 6: Random Forest
├── boosting_model.py                # Day 7: LightGBM
├── threshhold_optimization.py       # Day 8: Profit/Loss cost matrix
├── app.py                           # Day 9: Streamlit underwriting cockpit & TreeSHAP
├── audit_queries.sql                # Enterprise MySQL 8.4 risk queries & window functions
└── DAY-*-PROJECT-2-LOCK.md          # Daily build logs with verified metrics
```

## How to Run

```bash
# Install dependencies
pip install pandas numpy scikit-learn lightgbm streamlit matplotlib seaborn

# Launch the Streamlit underwriting cockpit
streamlit run app.py
```

## Tech Stack

Python · Pandas · NumPy · Scikit-Learn · LightGBM · MySQL 8.4 · Streamlit · Matplotlib · Seaborn

## Author

**Raj Dwarkanath Jadhav** — [GitHub](https://github.com/Rajjadhav555) · [LinkedIn](https://linkedin.com/in/raaj-jadhav)
