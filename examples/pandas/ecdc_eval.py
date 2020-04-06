import pandas as pd

d0 = pd.read_json("file:ecdc_cases.json")
# Removed the not needed any longer.
d0.drop(labels=["source", "original"], axis=1, inplace=True)
