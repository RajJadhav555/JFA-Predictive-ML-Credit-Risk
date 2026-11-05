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

threshholds = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.50]
print("\n==== Threshold & Profit Optimization Leaderboard ====")

for t in threshholds:
    approved = (y_probs < t)
    good_approved = np.sum((approved) & (y_test == 0))
    bad_approved = np.sum((approved) & (y_test == 1))
    net_profit = (good_approved * profit_per_good) - (bad_approved * loss_per_bad)

    total_approved = np.sum(approved)
    print(f"Throshhold: {t:.2f} | Approved: {total_approved:5d} | Good: {good_approved:5d} | Bad: {bad_approved:4d} | Net Profit: {net_profit:,.0f}")