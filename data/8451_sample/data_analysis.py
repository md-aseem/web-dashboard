import pandas as pd
import os

hhd_path = r"C:\Work\Courses\Intro to Cloud Computing\myflaskapp\data\8451_sample\400_households.csv"

df = pd.read_csv(hhd_path)

# Show the DataFrame
df.head()

print(df)