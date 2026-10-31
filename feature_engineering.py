import pandas as pd

df = pd.read_csv("data/credit_data_cleaned.csv", index_col=0)

df["TotalLateEvents"] = (
    df["NumberOfTime30-59DaysPastDueNotWorse"]
    + df["NumberOfTime60-89DaysPastDueNotWorse"]
    +  df["NumberOfTimes90DaysLate"]
)

print(f"Pristine Borrowers (0 Late Payments): {(df['TotalLateEvents'] == 0).sum():,}")
print(f"Distressed Borrowers (At least 1 Late): {(df['TotalLateEvents'] > 0).sum():,}")

df["PerCapitaIncome"] = df["MonthlyIncome"] / (df["NumberOfDependents"] + 1)

print(f"Median Per-Capita Income: ${df['PerCapitaIncome'].median():,.2f}")
print(f"Lowest 25% Household Cushion: ${df['PerCapitaIncome'].quantile(0.25):,.2f}")

df["HasLatePayment"] = (df["TotalLateEvents"] > 0).astype(int)

pristine_risk = df[df["HasLatePayment"] == 0]["SeriousDlqin2yrs"].mean() * 100
late_risk = df[df["HasLatePayment"] == 1]["SeriousDlqin2yrs"].mean() * 100

print(f"Default Risk for Pristine Borrowers: {pristine_risk:.2f}%")
print(f"Default Risk for Borrowers With Prior Late Mark: {late_risk:.2f}%")

df.to_csv("data/credit_data_engineered.csv")
print(f"\n Engineered Portfolio Successfully Saved: {len(df):,} borrowers ready for ML")