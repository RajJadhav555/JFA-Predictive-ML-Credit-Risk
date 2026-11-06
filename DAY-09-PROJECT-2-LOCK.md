# DAY 09: PRODUCTION UNDERWRITING SIMULATOR & INTERACTIVE DECISION COCKPIT (STREAMLIT)
**Date:** 2026-11-06  
**Operator:** Raj Dwarkanath Jadhav (Student ID #979948191, University of Auckland Feb 2027)  
**Project:** JFA-Predictive Credit Risk ML Engine  
**Working Directory:** `/media/raaj-jadhav/HDD/files/JFA_predictive/`  

---

## 1. Executive Summary & Objective
Transform the backend LightGBM machine learning model and profit-loss cost matrix (optimal threshold = 0.15, $30.58M net profit) into an interactive, production-grade web application (`app.py`) for credit risk officers and executive leadership.

---

## 2. Architectural Blueprint & Features

### A. Sub-Millisecond Inference Caching (`@st.cache_resource`)
- **Challenge:** Training LightGBM on 120,000 loans on every Streamlit page rerun creates 2-3s UI latency.
- **Solution:** Encapsulated model fitting and test-set precomputation inside `@st.cache_resource def load_engine()`. Model weights and test predictions remain locked in memory, delivering sub-millisecond slider responsiveness.

### B. Dynamic Executive Strategy Lens (Top Banner)
- **Unit Economics:** Embedded institutional payout matrix ($1,500 profit per performing loan vs -$10,000 write-off per default).
- **Reactive Slider:** Range 0.05 to 0.50, default locked at optimal **0.15**.
- **Live KPI Scoreboard (`st.columns(4)`):**
  - **Risk Cutoff:** Displays active threshold (e.g. `0.15`).
  - **Portfolio Net Profit:** Live dollar output (e.g. `$30,586,000`).
  - **Approval Rate:** Real-time acceptance percentage (e.g. `88.6%`).
  - **Defaults Allowed:** Exact volume of charge-offs permitted under active policy (e.g. `809`).

### C. Live Applicant Underwriting Desk (`st.form`)
- **Intake Form:** Captures age, monthly income, dependents, credit card utilization, debt ratio, open credit lines, real estate loans, and 30/60/90-day delinquencies.
- **Real-Time Feature Engineering:** Dynamically calculates:
  - `TotalLateEvents = past_due_30_59 + past_due_60_89 + late_90_days`
  - `HasLatePayment = 1 if TotalLateEvents > 0 else 0`
  - `PerCapitaIncome = monthly_income / (dependents + 1)`
  - `MonthlyIncome_Missing = 0`
- **Instant Decisioning:**
  - Case 1 (Prime Profile: 0 Delinquencies, 0.51 Utilization): Predicted Default Risk **5.83%** → **🟢 APPROVED**
  - Case 2 (Stress Test: Single 90+ Day Delinquency): Predicted Default Risk **18.60%** → **🔴 DECLINED** (exceeds 15.0% risk appetite)

---

## 3. Verified Production Metrics
- **Underwriting Execution Latency:** < 50ms
- **Streamlit Version:** 1.66.1
- **Target Deployment:** Local Port 8501
