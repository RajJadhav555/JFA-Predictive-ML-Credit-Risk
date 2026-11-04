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

y_preb_probs = model.predict_proba(X_test)[:, 1]
auc_score = roc_auc_score(y_test, y_preb_probs)

print(f"\n==== Model Showdown Leaderboard ====")
print(f"1. Baseline Logistic Regerssion : 0.8549")
print(f"2. Random Forest (100 Trees)    : 0.8686")
print(f"3. LightGBM Gredient Boosting   : {auc_score:.4f}")