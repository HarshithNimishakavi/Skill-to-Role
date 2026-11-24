import pandas as pd

# Load dataset
df = pd.read_csv("data/student_dataset.csv")

# Remove student ID
df = df.drop(columns=["student_id"])

# Check missing values
print("Missing values:")
print(df.isnull().sum().sum())

# Check duplicate rows
print("\nDuplicate rows:")
print(df.duplicated().sum())

# Check final shape
print("\nFinal dataset shape:")
print(df.shape)

# Display first 5 rows
print("\nFirst 5 rows:")
print(df.head())