# 🏆 DAY 24 / PROJECT 2 (DAY 7) LOCKED: GRADIENT BOOSTING & THREE-MODEL BENCHMARK SHOWDOWN
**Date:** 2026-11-04  
**Conversation ID:** `c611b645-2123-457a-b5a2-b9e9caa2db8f` (resumed from `014ae1a0-e730-4d96-b4e4-cb81d0be9212`)  
**Operator:** Raj Dwarkanath Jadhav  
**Mission:** Operation Auckland (Target: Quantitative Risk-Tech / Credit Risk / Fraud Analytics)

---

## 🏛️ The Auckland Interview Narrative (3 Sentences)
> 1. *"To capture high-order feature interactions and correct subtle residual errors on borderline applicants, we deployed a sequential Gradient Boosting architecture (`LGBMClassifier`, 100 estimators, learning rate = 0.05)."*
> 2. *"Evaluated on our frozen vault of 30,000 unseen test borrowers, LightGBM achieved our portfolio's all-time peak **AUC-ROC of 0.8699**, outperforming both our 0.8549 Logistic Regression baseline and our 0.8686 Random Forest ensemble."*
> 3. *"In our production MySQL audit across 150,000 accounts, we proved that crossing the statutory 90-day delinquency threshold triggers a catastrophic **7.2x risk explosion (4.63% to 33.66%)**, empirically validating why gradient-boosted decision trees allocate aggressive splitting priority to severe delinquency signals."*

---

## 📊 Quantitative Modeling Milestones

| Component | Engineering Implementation | Portfolio Metric | Risk / Business Significance |
| :--- | :--- | :--- | :--- |
| **MySQL 90-Day Heavy-Bag** | `CASE WHEN late_90_days = 0 ...` | **Clean: 4.63%**<br>**Single 90-Day: 33.66%**<br>**Chronic: 55.15%** | Self-formulated and executed across 150k loans in 0.09s, proving that severe delinquency represents a non-linear statutory cliff (Basel Stage 3). |
| **Sequential Boosting Engine** | `LGBMClassifier(n_estimators=100, learning_rate=0.05, n_jobs=-1)` | **100 Sequential Trees** | Sequentially corrects residual underwriting errors on hard-to-classify edge borrowers with ultra-low memory overhead. |
| **Model Discrimination Showdown** | `roc_auc_score(y_test, y_pred_probs)` | **AUC-ROC: 0.8699** | **+1.50% (+0.0150) cumulative lift** over baseline, delivering institutional peak ranking power on 30,000 unseen test applicants. |
| **Comparative Leaderboard** | Three-Model Head-to-Head | **LogReg: 0.8549**<br>**RF: 0.8686**<br>**LightGBM: 0.8699** | Full institutional model lineage established under identical stratified 80/20 train/test conditions (`random_state=42`). |

---

## 🛠️ Code Implemented (`boosting_model.py`)
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
from sklearn.metrics import roc_auc_score

df = pd.read_csv("data/credit_data_engineered.csv", index_col=0)

X = df.drop(columns=["SeriousDlqin2yrs"])
y = df["SeriousDlqin2yrs"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

model = LGBMClassifier(
    n_estimators=100,
    learning_rate=0.05,
    random_state=42,
    n_jobs=-1,
    verbose=-1
)

model.fit(X_train, y_train)

y_pred_probs = model.predict_proba(X_test)[:, 1]
auc_score = roc_auc_score(y_test, y_pred_probs)

print(f"\n==== Model Showdown Leaderboard ====")
print(f"1. Baseline Logistic Regression : 0.8549")
print(f"2. Random Forest (100 Trees)    : 0.8686")
print(f"3. LightGBM Gradient Boosting   : {auc_score:.4f}")
```
