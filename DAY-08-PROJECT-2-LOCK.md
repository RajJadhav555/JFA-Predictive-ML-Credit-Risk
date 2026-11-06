# 🏆 DAY 25 / PROJECT 2 (DAY 8) LOCKED: THRESHOLD OPTIMIZATION & PROFIT/LOSS COST MATRIX
**Date:** 2026-11-05  
**Conversation ID:** `4f165bc9-1389-46b2-b0e4-14ac16754626` (bridged from `c611b645-2123-457a-b5a2-b9e9caa2db8f` & `b8fc73bd-9f81-4fc7-ac41-de51e6e0ecbf`)  
**Operator:** Raj Dwarkanath Jadhav  
**Mission:** Operation Auckland (Target: Quantitative Risk-Tech / Credit Risk / Fraud Analytics)  
**Git Commit Hash:** `871e310`

---

## 🏛️ The Auckland Interview Narrative (3 Sentences)
> 1. *"In credit risk, defaults carry severe asymmetric costs—a bad loan charge-off (-$10,000) hurts 6.6x more than the profit of a good loan (+$1,500), making standard 0.50 classification cutoffs financially reckless."*
> 2. *"By evaluating our LightGBM model across 30,000 unseen test borrowers with an institutional profit/loss cost matrix, we mapped the empirical dollar curve and proved that the optimal decision threshold is **0.15**."*
> 3. *"Calibrating our underwriting cutoff to 0.15 maximizes net bank profit at **$30,586,000**—delivering a **+$5,256,500 (+20.7%) bottom-line lift** over the textbook 0.50 cutoff while cutting portfolio default write-offs in half (815 fewer defaults)."*

---

## 📊 Quantitative Modeling & Financial Optimization Milestones

| Component | Engineering Implementation | Portfolio Metric | Risk / Business Significance |
| :--- | :--- | :--- | :--- |
| **MySQL Policy Trap Audit** | `CASE WHEN (past_due_30_59 + ...) = 0 ...` | **Approved: 2.73% default**<br>**Rejected: 22.27% default** | Self-formulated and executed in 0.09s, proving that blunt zero-tolerance policies discard 23,600 paying borrowers ($118M lost gross volume). |
| **Auckland Unit Economics** | `$1,500 Good Profit / $10,000 Bad Loss` | **Asymmetric Risk Ratio: 6.67x** | Accurately models the financial imbalance where write-offs dwarf interest margins. |
| **Vectorized Profit Engine** | `(good_approved * 1500) - (bad_approved * 10000)` | **30,000 Test Borrowers Evaluated** | Instantly calculates exact bank net revenue across candidate probability thresholds in memory. |
| **Threshold Optimization Curve** | Candidate thresholds: `[0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.50]` | **Optimal Threshold: 0.15**<br>**Peak Profit: $30,586,000** | Proves the sweet spot where the bank captures 25,784 good loans while strictly capping bad loans at 809. |
| **Financial Delta vs Default 0.50** | Cutoff Comparison (0.15 vs 0.50) | **+$5,256,500 Net Profit Lift (+20.7%)**<br>**815 Fewer Charge-Offs** | Empirically proves the business value of quantitative threshold tuning for Chief Risk Officers and Credit Committees. |

---

## 🛠️ Code Implemented (`threshold_optimization.py`)
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier

df = pd.read_csv("data/credit_data_engineered.csv", index_col=0)

X = df.drop(columns=["SeriousDlqin2yrs"])
y = df["SeriousDlqin2yrs"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

model = LGBMClassifier(
    n_estimators=100, learning_rate=0.05, random_state=42, n_jobs=-1, verbose=-1
)
model.fit(X_train, y_train)

y_probs = model.predict_proba(X_test)[:, 1]

profit_per_good = 1500
loss_per_bad = 10000

thresholds = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.50]
print("\n==== Threshold & Profit Optimization Leaderboard ====")

for t in thresholds:
    approved = (y_probs < t)
    good_approved = np.sum((approved) & (y_test == 0))
    bad_approved = np.sum((approved) & (y_test == 1))
    net_profit = (good_approved * profit_per_good) - (bad_approved * loss_per_bad)
    total_approved = np.sum(approved)
    print(f"Threshold: {t:.2f} | Approved: {total_approved:5d} | Good: {good_approved:5d} | Bad: {bad_approved:4d} | Net Profit: ${net_profit:,.0f}")
```
