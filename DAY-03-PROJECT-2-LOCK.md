# 🏆 DAY 20 / PROJECT 2 (DAY 3-4) LOCKED: FEATURE ENGINEERING & DELINQUENCY VELOCITY
**Date:** 2026-10-31  
**Conversation ID:** `e27ba901-b061-4ae3-b3b0-f05ecae90845` (continued from `be7fd574-b484-40ab-8d19-627aff11c9f8`)  
**Operator:** Raj Dwarkanath Jadhav  
**Mission:** Operation Auckland (Target: Quantitative Risk-Tech / Credit Risk / Fraud Analytics)

---

## 🏛️ The Auckland Interview Narrative (3 Sentences)
> 1. *"In retail portfolio risk modeling, raw static features mask the behavioral dynamics of borrower distress."*
> 2. *"We engineered three domain-specific risk signals: cumulative delinquency velocity (`TotalLateEvents`), per-capita household income cushion (`PerCapitaIncome`), and an explicit binary delinquency flag (`HasLatePayment`)."*
> 3. *"Empirical validation on our 150,000-borrower portfolio revealed that prior late payment marks trigger an **8.15x surge in default risk (22.27% vs 2.73%)**, providing our upcoming ML classification model with its sharpest early-warning feature."*

---

## 📊 Quantitative Feature Metrics

| Engineered Feature | Mathematical Formula | Key Portfolio Metric | Risk / Business Significance |
| :--- | :--- | :--- | :--- |
| **`TotalLateEvents`** | `Late30_59 + Late60_89 + Late90` | **119,637 Pristine (79.8%)** vs **30,362 Late (20.2%)** | Consolidates fragmented delinquency records into a single cumulative behavioral velocity indicator. |
| **`PerCapitaIncome`** | `MonthlyIncome / (Dependents + 1)` | **Median: $4,000.00**<br>**Q1 (Lowest 25%): $2,151.00** | Measures real disposable household cushion per human; bottom 25% live under $2,151/person and represent the primary vulnerability cluster under macro inflation. |
| **`HasLatePayment`** | `(TotalLateEvents > 0).astype(int)` | **Pristine Risk: 2.73%**<br>**Delinquent Risk: 22.27%** | Binary risk flag revealing an **8.15x jump in default probability** between pristine and impaired borrowers. |
| **Export File** | — | `data/credit_data_engineered.csv` | Persisted 149,999 institutional records ready for ML train/test splitting and model benchmark. |

---

## 🛠️ Code Implemented (`feature_engineering.py`)
```python
import pandas as pd

df = pd.read_csv("data/credit_data_cleaned.csv", index_col=0)

df["TotalLateEvents"] = (
    df["NumberOfTime30-59DaysPastDueNotWorse"]
    + df["NumberOfTime60-89DaysPastDueNotWorse"]
    + df["NumberOfTimes90DaysLate"]
)

print(f"Pristine Borrowers (0 Late Payments): {(df['TotalLateEvents'] == 0).sum():,}")
print(f"Distressed Borrowers (At least 1 Late): {(df['TotalLateEvents'] > 0).sum():,}")

df["PerCapitaIncome"] = df["MonthlyIncome"] / (df["NumberOfDependents"] + 1)

print(f"Median Per-Capita Income: ${df['PerCapitaIncome'].median():,.2f}")
print(f"Lowest 25% Household Cushion: ${df['PerCapitaIncome'].quantile(0.25):,.2f}")

df["HasLatePayment"] = (df["TotalLateEvents"] > 0).astype(int)

pristine_risk = df[df["HasLatePayment"] == 0]["SeriousDlqin2yrs"].mean() * 100
late_risk = df[df["HasLatePayment"] == 1]["SeriousDlqin2yrs"].mean() * 100

print(f"Default Risk for Pristine Borrowers: {pristine_risk:.2f}%")
print(f"Default Risk for Borrowers With Prior Late Mark: {late_risk:.2f}%")

df.to_csv("data/credit_data_engineered.csv")
print(f"\nEngineered Portfolio Successfully Saved: {len(df):,} borrowers ready for ML")
```
