# 🏆 DAY 21 / PROJECT 2 (DAY 5) LOCKED: STRATIFIED SPLIT & LOGISTIC BENCHMARK
**Date:** 2026-11-01  
**Conversation ID:** `d304bd90-064b-44df-9145-719ffd4f4083` (resumed from `e27ba901-b061-4ae3-b3b0-f05ecae90845`)  
**Operator:** Raj Dwarkanath Jadhav  
**Mission:** Operation Auckland (Target: Quantitative Risk-Tech / Credit Risk / Fraud Analytics)

---

## 🏛️ The Auckland Interview Narrative (3 Sentences)
> 1. *"To prevent data leakage and account for extreme portfolio class imbalance (6.68% default rate), we partitioned 150,000 borrower profiles using an 80/20 stratified train/test split."*
> 2. *"We standardized heterogeneous feature scales with `StandardScaler` to align dollar incomes with delinquency event counts, and trained a baseline Logistic Regression model adhering to Basel/RBNZ explainability standards."*
> 3. *"Evaluated on 30,000 completely unseen test applicants, our baseline model achieved an institutional-grade **AUC-ROC of 0.8549**, establishing a rigorous benchmark for our upcoming non-linear ensemble models."*

---

## 📊 Quantitative Modeling Milestones

| Component | Engineering Implementation | Portfolio Metric | Risk / Business Significance |
| :--- | :--- | :--- | :--- |
| **MySQL Stratification** | `CASE WHEN utilization < 0.3 ...` | **Low Risk: 2.22%**<br>**High Risk: 21.08%** | Direct empirical proof in MySQL: utilization >80% surges default risk nearly 10x; aggregated in 0.11s. |
| **Stratified Split** | `train_test_split(..., test_size=0.20, stratify=y)` | **Train: 119,999 (6.68%)**<br>**Test: 30,000 (6.68%)** | Guarantees train and vault test sets preserve the exact baseline default distribution without variance distortion. |
| **Feature Scaling** | `StandardScaler()` (`fit_transform` train, `transform` test) | **Z-Score Normalization** | Prevents large magnitude features (income, debt ratio) from dwarfing sensitive delinquency signals during gradient optimization. |
| **Baseline Model** | `LogisticRegression(max_iter=1000)` | **AUC-ROC: 0.8549** | Institutional grade baseline (>0.80) providing fully interpretable odds ratios and transparent adverse action reasons. |

---

## 🛠️ Code Implemented (`baseline_model.py`)
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

df = pd.read_csv("data/credit_data_engineered.csv", index_col=0)

x = df.drop(columns=["SeriousDlqin2yrs"])
y = df["SeriousDlqin2yrs"]

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set : {len(x_train):,} | Test set : {len(x_test):,}")
print(f"Train Default : {y_train.mean() * 100:.2f}% | Test Default : {y_test.mean() * 100:.2f}%")

scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(x_train_scaled, y_train)

print(f"\n----- Model Trained Successfully on 119,999 Borrowers -----")

y_pred_proba = model.predict_proba(x_test_scaled)[:, 1]
auc_score = roc_auc_score(y_test, y_pred_proba)

print(f"\nBaseline Logistics Regression AUC-ROC: {auc_score:.4f}")
```
