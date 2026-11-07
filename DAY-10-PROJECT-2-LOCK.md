# DAY 10: ENTERPRISE SQL PILLAR — RBNZ LEVERAGE STRESS AUDIT & DYNAMIC FEATURE PERSISTENCE
**Date:** 2026-11-07  
**Operator:** Raj Dwarkanath Jadhav (Student ID #979948191, University of Auckland Feb 2027)  
**Project:** JFA-Predictive Credit Risk ML Engine (Enterprise SQL Track)  
**Database:** MySQL 8.4 (`credit.borrowers` — 149,999 records)  
**Working Directory:** `/media/raaj-jadhav/HDD/files/JFA_predictive/`  

---

## 1. Executive Scenario & Core Objective
Audit whether high monthly income insulates borrowers from high debt burden, as assumed by traditional underwriting, or whether high debt ratios trigger default risk regardless of income. Address the "Undisclosed Income" segment (29,731 borrowers) on a single executive plate to ensure zero portfolio blind spots.

---

## 2. Key Architectural Upgrades & Findings

### A. Dynamic Database Feature Persistence (`STORED GENERATED COLUMN`)
- **Challenge:** Repeatedly calculating delinquency sum `(past_due_30_59 + late_90_days + past_due_60_89)` creates query latency and cognitive fatigue.
- **Solution:** Upgraded table schema with a production `STORED GENERATED COLUMN`:
  ```sql
  ALTER TABLE borrowers 
  ADD COLUMN total_late_events INT 
  GENERATED ALWAYS AS (past_due_30_59 + late_90_days + past_due_60_89) STORED;
  ```
- **Performance:** 149,999 rows recalculated and indexed in **0.73 seconds**.

### B. The "Thin File" Paradox (Undisclosed Income Audit)
- Analyzed 29,731 borrowers with unrecorded income (`monthly_income_missing = 1`).
- **Counter-Intuitive Discovery:** Borrowers with $\le 2$ open credit lines default at **10.25% - 12.63%** (more than double the baseline), whereas borrowers with $\ge 3$ lines default at **4.64%**.
- **Root Cause:** In subprime credit, $\le 2$ open lines when income is missing indicates a "Thin File" or credit-restricted borrowers whose lines were shut down by other lenders.
- **Extreme Stress Risk:** When combined with a single past delinquency, default risk explodes to **37.41%**.

### C. SQL Name Collision & Alias Shadowing Resolution
- **Gotcha:** Giving a calculated `CASE` expression the identical alias `AS 'debt_ratio'` caused MySQL to prioritize the underlying decimal column `borrowers.debt_ratio`, generating 116,094 rows with count = 1.
- **Resolution:** Decoupled alias to `debt_tier`, resolving parser ambiguity and reducing query runtime from 2.5 minutes down to **0.12 seconds**.

### D. The 8-Row Unified Executive Risk Matrix (Ground Truth)
```sql
SELECT 
  CASE 
    WHEN monthly_income_missing = 1 THEN '4. Undisclosed Income' 
    WHEN monthly_income >= 6000 THEN '1. High Income' 
    WHEN monthly_income >= 3000 THEN '2. Middle Income' 
    ELSE '3. Low Income' 
  END AS income_tier, 
  CASE  
    WHEN debt_ratio > 0.50 THEN 'High Debt' 
    ELSE 'Managable Debt' 
  END AS debt_tier, 
  COUNT(*) AS total_borrowers, 
  ROUND(AVG(serious_dlq_2yrs) * 100, 2) AS default_rate_pct 
FROM borrowers 
GROUP BY income_tier, debt_tier 
ORDER BY income_tier, debt_tier;
```

#### Empirical Results (Execution Time: 0.12s):
| Income Tier | Debt Tier | Total Borrowers | Default Rate (%) | Risk Diagnosis |
| :--- | :--- | :--- | :--- | :--- |
| **1. High Income ($\ge \$6\text{k}$)** | **High Debt ($> 50\%$)** | 7,744 | **10.36%** | **+140% Risk Surge** (Worse than low-income safe!) |
| **1. High Income ($\ge \$6\text{k}$)** | **Manageable Debt ($\le 50\%$)** | 45,384 | **4.30%** | Prime Baseline Portfolio |
| **2. Middle Income ($\$3\text{k}-\$6\text{k}$)** | **High Debt ($> 50\%$)** | 11,030 | **11.01%** | **Highest Risk Segment in Entire Bank** |
| **2. Middle Income ($\$3\text{k}-\$6\text{k}$)** | **Manageable Debt ($\le 50\%$)** | 32,784 | **6.96%** | Standard Performing Portfolio |
| **3. Low Income ($< \$3\text{k}$)** | **High Debt ($> 50\%$)** | 9,409 | **8.45%** | Highly Stressed Segment |
| **3. Low Income ($< \$3\text{k}$)** | **Manageable Debt ($\le 50\%$)** | 13,917 | **9.43%** | Lower Capacity Segment |
| **4. Undisclosed Income** | **High Debt ($> 50\%$)** | 28,109 | **5.55%** | Commercial / Self-Employed Tier |
| **4. Undisclosed Income** | **Manageable Debt ($\le 50\%$)** | 1,622 | **6.72%** | Moderate Risk Pocket |

---

## 3. Auckland Interview Power Story
> 1. *"In credit underwriting, traditional lenders often assume a large monthly salary insulates a borrower from default, but our leverage audit tested whether high income actually protects against high debt ratios."*  
> 2. *"By architecting a multi-dimensional matrix in MySQL across 150,000 borrowers, we proved that high earners making over $6,000/month with high debt ratios experience a 140% surge in default risk—exploding from 4.30% up to 10.36%."*  
> 3. *"This proved that high cash flow cannot compensate for excessive leverage, allowing our credit committee to implement strict debt-to-income caps across all salary bands before bad debt hits the balance sheet."*
