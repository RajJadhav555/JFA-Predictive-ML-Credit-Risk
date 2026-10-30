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

df = df[df["age"]>= 18]
df["RevolvingUtilizationOfUnsecuredLines"] = df["RevolvingUtilizationOfUnsecuredLines"].clip(upper=2.0)
df.to_csv("data/credit_data_cleaned.csv")

print(f"\n--- Cleaned Portfolio Summary---")
print(f"Cleaned Borrower's Count: {len(df):,}")
print(f"New Max Utilization: {df['RevolvingUtilizationOfUnsecuredLines'].max():.2f}")
print(f"New Minimum Age: {df['age'].min()} years old")