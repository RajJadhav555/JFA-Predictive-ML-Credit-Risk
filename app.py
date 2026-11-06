import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="JFA Underwriting Cockpit", layout="wide")
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split

@st.cache_resource

def load_engine():
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
        return model, X, y_probs, y_test

model, X, y_probs, y_test = load_engine()

st.title("🏛️ JFA Credit Risk & Predictive Underwriting Cockpit")
st.markdown("### Executive Strategy: Portfolio Threshold Optimization")
profit_per_good = 1500
loss_per_bad = 10000

threshold = st.slider(
        "Select Default Risk Tolerance Cutoff (Threshold)", 0.05, 0.50, 0.15, 0.01
)
approved = y_probs < threshold
good_approved = np.sum((approved) & (y_test == 0))
bad_approved = np.sum((approved) & (y_test == 1))
net_profit = (good_approved * profit_per_good) - (bad_approved * loss_per_bad)
approval_rate = (np.sum(approved) / len(y_test)) * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Risk Cutoff", f"{threshold:.2f}")
col2.metric("Portfolio Net Profit", f"${net_profit:,.0f}")
col3.metric("Approval Rate", f"{approval_rate:.1f}%")
col4.metric("Defaults Allowed", f"{bad_approved:,}")

st.divider()
st.markdown("### 📋 Live Applicant Underwriting Desk")

with st.form("underwrite_form"):
    colA, colB = st.columns(2)
    with colA:
            st.subheader("Financial Profile")
            age = st.number_input("Age", min_value=18, max_value=100, value=35)
            monthly_income = st.number_input("Monthly Income ($)", min_value=0.0, value=5500.0, step=500.0)
            dependents = st.number_input("Number of Dependents", min_value=0, max_value=20, value=1)
            utilization = st.slider("Credit Card Utilization Ratio", 0.0, 2.0, 0.30, 0.01)
    with colB:
            st.subheader("Credit & Repayment History")
            debt_ratio = st.number_input("Debt Ratio", min_value=0.0, max_value=5.0, value=0.35, step=0.05)
            open_lines = st.number_input("Open Credit Lines / Loans", min_value=0, max_value=50, value=6)
            real_estate_loans = st.number_input("Real Estate Loans / Mortgages", min_value=0, max_value=20, value=1)
            past_due_30_59 = st.number_input("30-59 Days Past Due Count", min_value=0, max_value=20, value=0)
            past_due_60_89 = st.number_input("60-89 Days Past Due Count", min_value=0, max_value=20, value=0)
            late_90_days = st.number_input("90+ Days Delinquency Count", min_value=0, max_value=20, value=0)

            submitted = st.form_submit_button("🔍 Run Underwriting Assessment")
    if submitted:
        total_late = past_due_30_59 + past_due_60_89 + late_90_days
        has_late = 1 if total_late > 0 else 0
        per_capita = monthly_income / (dependents + 1)
        applicant_row = [
            utilization, age, past_due_30_59, debt_ratio, monthly_income,
            open_lines, late_90_days, real_estate_loans, past_due_60_89,
            dependents, 0, total_late, per_capita, has_late
        ]
        applicant_df = pd.DataFrame([applicant_row], columns=X.columns)
        prob = model.predict_proba(applicant_df)[0, 1]
        st.markdown("---")
        if prob < threshold:
            st.success(
                f"🟢 **APPROVED** — Default Risk: **{prob*100:.2f}%** (Tolerance: {threshold*100:.1f}%)"
            )
        else:
            st.error(
                f"🔴 **DECLINED** — Default Risk: **{prob*100:.2f}%** (Tolerance: {threshold*100:.1f}%)"
            )