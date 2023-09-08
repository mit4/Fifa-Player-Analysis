import pandas as pd
from pandas_profiling import ProfileReport

data = pd.read_csv("../../data/players_21.csv")

profile = ProfileReport(df=data)
profile.to_file(output_file="../../reports/Pre Profiling Report.html")
print("Accomplished!")
