import pandas as pd
a=pd.read_csv("data/student_dataset.csv")

#dropping the unwanted columns
a=a.drop(columns=["student_id"])

#splitting the input and output features

x=a.iloc[:,:-1]
y=a['career_role']

print(x.shape)
print(y.shape)

#writing the columns

print(x.columns.tolist())
print(y.value_counts())
