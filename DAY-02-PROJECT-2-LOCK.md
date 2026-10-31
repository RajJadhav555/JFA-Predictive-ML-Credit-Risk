# 🏆 DAY 18 / PROJECT 2 (DAY 2) LOCKED: DATA HYGIENE, IMPUTATION & OUTLIER MITIGATION
**Date:** 2026-10-30  
**Conversation ID:** `614eca1a-9bfa-485e-8586-2b7e2cd5b13f`  
**Authentic Git Commit Hash:** `4203fc0`  
**Operator:** Raj Dwarkanath Jadhav  
**Mission:** Operation Auckland (Target: Quantitative Risk-Tech / Credit Risk / Fraud Analytics)

---

## 🏛️ The Auckland Interview Narrative (3 Sentences)
> 1. *"In retail portfolio modeling, discarding 29,731 unrecorded incomes would introduce severe sample selection bias and forfeit 20% of addressable loan demand."*
> 2. *"To solve this, we engineered a dual-layer defense: **Median Imputation** ($5,400.00) to preserve mathematical stability, paired with a binary **Missingness Indicator Flag (`MonthlyIncome_Missing = 1`)**."*
> 3. *"We cleansed the portfolio of operational glitches by filtering invalid infant records (`age >= 18`) and Winsorizing extreme revolving utilization from 50,708 down to a 2.00 cap, preserving 149,999 institutional-grade loan records."*

---

## 📊 Quantitative Production Metrics

| Risk Dimension | Raw Ingest Baseline | Cleaned Production Target | Resolution Mechanism |
| :--- | :--- | :--- | :--- |
| **Total Borrowers** | 150,000 | **149,999** | Filtered 1 invalid infant record (`age = 0`) |
| **Missing Monthly Incomes** | 29,731 | **0** | Imputed with portfolio median (\$5,400.00) |
| **Missing Dependents** | 3,924 | **0** | Imputed with median (0 dependents) |
| **Missing Income Spy Flag** | 0 | **29,731** | Binary feature (`MonthlyIncome_Missing = 1`) |
| **Max Credit Utilization** | 50,708.0 | **2.00** | Clipped / Winsorized to 2.00 (200% stress ceiling) |
| **Minimum Borrower Age** | 0 years old | **21 years old** | Enforced legal borrowing threshold (`>= 18`) |
| **Export File** | — | `data/credit_data_cleaned.csv` | Persisted to disk for Feature Engineering |

---

## 🛠️ Code Implemented (`data_cleaning.py`)
```python
import pandas as pd

df = pd.read_csv("data/credit_data.csv", index_col=0)

income_median = df["MonthlyIncome"].median()
dependents_median = df["NumberOfDependents"].median()

print(f"Monthly Income Median: ${income_median:,.2f}")
print(f"Number of Dependents Median: {dependents_median:.0f}")

df["MonthlyIncome_Missing"] = df["MonthlyIncome"].isnull().astype(int)
df["MonthlyIncome"] = df["MonthlyIncome"].fillna(income_median)
df["NumberOfDependents"] = df["NumberOfDependents"].fillna(dependents_median)

print(f"Remaining Missing Income: {df['MonthlyIncome'].isnull().sum()}")
print(f"Missing Income Flags Created: {df['MonthlyIncome_Missing'].sum():,}")

print(f"Max Credit Utilization: {df['RevolvingUtilizationOfUnsecuredLines'].max():,.0f}")
print(f"99th Percentile Utilization: {df['RevolvingUtilizationOfUnsecuredLines'].quantile(0.99):.2f}")
print(f"Minimum Age in Portfolio: {df['age'].min()} years old")

df = df[df["age"] >= 18]
df["RevolvingUtilizationOfUnsecuredLines"] = df["RevolvingUtilizationOfUnsecuredLines"].clip(upper=2.0)
df.to_csv("data/credit_data_cleaned.csv")

print(f"\n--- Cleaned Portfolio Summary ---")
print(f"Cleaned Borrower's Count: {len(df):,}")
print(f"New Max Utilization: {df['RevolvingUtilizationOfUnsecuredLines'].max():.2f}")
print(f"New Minimum Age: {df['age'].min()} years old")
```

---

## 🔒 Permanent Core Principles Reaffirmed
1. **Architectural Purity (No "Fifth Wheel"):** Side skills (e.g., SQL, Power BI) must never derail or hijack the primary engineering blueprint. They are introduced only when the pipeline architecture naturally requires them, keeping the core vehicle balanced and high-velocity.
2. **Mastery of `f-string` Syntax:** `{ variable : instructions }` — comma for thousands (`:,`), dot for decimals, `f` for float precision (`.2f`).
3. **Next Milestone (Day 19 / Project 2 - Day 3):** Feature Engineering — Debt-to-Income interaction variables, delinquency velocity indicators, and feature distribution scaling.
