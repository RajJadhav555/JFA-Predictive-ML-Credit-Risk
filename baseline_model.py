import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score 

df = pd.read_csv("data/credit_data_engineered.csv", index_col=0)

x = df.drop(columns=["SeriousDlqin2yrs"])
y = df["SeriousDlqin2yrs"]

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size = 0.2, random_state = 42, stratify = y
)

print(f"Training set : {len(x_train):,} | Test set : {len(x_test):,}")
print(f"Train Default : {y_train.mean() * 100:.2f}% | Test Default : {y_test.mean() * 100:.2f}%")

scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

model = LogisticRegression(max_iter = 1000, random_state = 42)
model.fit(x_train_scaled, y_train)

print(f"\n----- Model Trained Successfully on 119,999 Borrowers ------")

y_pred_proba = model.predict_proba(x_test_scaled)[:, 1]
auc_score = roc_auc_score(y_test, y_pred_proba)

print(f"\n Baseline Logistics Regression AUC-ROC: {auc_score:.4f}")