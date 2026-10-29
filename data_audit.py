import pandas as pd

df = pd.read_csv("data/credit_data.csv", index_col=0)

target = "SeriousDlqin2yrs"
default_count = df[target].value_counts()
default_rate = df[target].mean() * 100

print(f"Total Borrowes : {len(df):,}")
print(f"Repaid (0): {default_count[0]:,} | Defaulted (1): {default_count[1]:,}")
print(f"Baseline Portfolio Default Rate: {default_rate:.2f}%")

missing = df.isnull().sum()
print("\n----- Missing Data Audit ----")
print(missing[missing >0])