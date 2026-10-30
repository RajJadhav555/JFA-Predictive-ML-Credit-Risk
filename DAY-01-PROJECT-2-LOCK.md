# 🏛️ OPERATION AUCKLAND — PROJECT 2 (DAY 1) IMMORTALIZED RECORD
**Date:** October 29, 2026  
**Operator:** Raj Dwarkanath Jadhav  
**Mission Status:** PROJECT 2 DAY 1 LOCKED 🇳🇿  
**Authentic Git Commit:** `88396f2`  
**Active Repository:** `/media/raaj-jadhav/HDD/files/JFA_predictive`

---

## 🎯 Executive Summary & Milestone Achieved
Raj officially inaugurated **Project 2: JFA-Predictive (Machine Learning Credit Risk & Default Prediction Engine)**.

Instead of drifting into developer feature-creep, Raj exercised strategic discipline, called out the roadmap milestone, and pivoted directly to weaponizing his machine learning capabilities.

---

## 🧠 What Was Mastered & Implemented

### 1. Ingestion of the 150,000-Borrower Gold Standard Dataset
* Ingested Kaggle's industry benchmark *"Give Me Some Credit"* dataset (`credit_data.csv`).
* Mapped retail banking features including `DebtRatio` (FOIR), `RevolvingUtilizationOfUnsecuredLines`, `age`, and 30/60/90-day delinquency counts.

### 2. Baseline Default Rate & Class Imbalance Audit (`data_audit.py`)
* Isolated the binary target: `SeriousDlqin2yrs` (1 = Default, 0 = Repaid).
* Vectorized default frequency calculation:
  * **Repaid (0):** 139,974 borrowers (93.32%)
  * **Defaulted (1):** 10,026 borrowers (6.68%)
  * **Baseline Portfolio Default Rate:** **6.68%**
* Recognized the fundamental **Class Imbalance** challenge in banking: why naive accuracy metrics fail and why specialized loss functions/metrics (ROC-AUC, Precision-Recall) are mandatory.

### 3. Missing Data Forensic Audit
* Discovered missing data across only two attributes:
  * **`MonthlyIncome`**: missing for **29,731 applicants** (19.82%).
  * **`NumberOfDependents`**: missing for **3,924 applicants** (2.62%).
* Articulated the business rationale against naive row deletion (`dropna()`): avoiding survivorship bias and preserving the self-employed/gig borrower segment.

---

## 🎤 Auckland Interview Ready Story (3-Sentence Pitch)
> *"In launching my predictive credit risk engine, I initiated an exploratory data audit on a 150,000-borrower historical retail loan dataset, identifying an underlying 6.68% portfolio default rate. I diagnosed severe class imbalance and revealed that nearly 20% of applicants lacked disclosed monthly income. Rather than naively discarding nearly 30,000 borrower profiles and introducing survivorship bias, I architected a data auditing pipeline to prepare this unrecorded segment for deliberate credit risk imputation and Weight of Evidence scorecard binning."*

---

## 📈 Git Repository Integrity
```bash
commit 88396f2
Author: Raj Jadhav
Date:   Thu Oct 29 2026

    Day 1 (Project 2): Ingest 150k benchmark lon dataset, audit 6.68% baseline default rate, and map missing income gaps
```
