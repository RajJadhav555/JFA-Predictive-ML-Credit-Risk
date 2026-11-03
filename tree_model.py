import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

df = pd.read_csv("data/credit_data_engineered.csv")

features = [
    "RevolvingUtilizationOfUnsecuredLines",
    "age",
    "DebtRatio",
    "MonthlyIncome",
    "NumberOfOpenCreditLinesAndLoans",
    "NumberRealEstateLoansOrLines",
    "NumberOfDependents",
    "MonthlyIncome_Missing",
    "TotalLateEvents",
    "PerCapitaIncome",
    "HasLatePayment",
    "NumberOfTime30-59DaysPastDueNotWorse",
    "NumberOfTime60-89DaysPastDueNotWorse",
    "NumberOfTimes90DaysLate"
]

X = df[features]
y = df["SeriousDlqin2yrs"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

rf_model = RandomForestClassifier(n_estimators= 100, max_depth= 10, n_jobs=-1)
rf_model.fit(X_train, y_train)

y_pred_probs = rf_model.predict_proba(X_test)[:, 1]
auc_score = roc_auc_score(y_test, y_pred_probs)

print(f"\n==== Random Forest AUC-ROC: {auc_score:.4f} =====")

importance = pd.Series(rf_model.feature_importances_, index= features).sort_values(ascending=False)
print("\n Top 5 Risk Drivers (Gini Importance):")
print(importance.head(5))