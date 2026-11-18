import pandas as pd
df = pd.read_csv("data/student_dataset.csv")

# First 5 rows
print("FIRST 5 ROWS")
print(df.head())

# Dataset shape
print("\nDATASET SHAPE")
print(df.shape)

# Column names
print("\nCOLUMNS")
print(df.columns.tolist())

# Data types
print("\nDATA TYPES")
print(df.dtypes)

# Missing values
print("\nMISSING VALUES")
print(df.isnull().sum())

# Duplicate rows
print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

# Career role distribution
print("\nCAREER ROLE DISTRIBUTION")
print(df["career_role"].value_counts())