import numpy as np
import pandas as pd
from baseline_model import model, x

weights = model.coef_[0]

importance_df = pd.DataFrame({
    "Feature" : x.columns,
    "Weight" : weights,
    "Risk_Multiplier" : np.exp(weights)   
})

importance_df = importance_df.sort_values(by="Weight", ascending=False)

print("\n==== TOP CREDIT DEFALUT RISK DRIVERS =====")
print(importance_df.to_string(index=False))