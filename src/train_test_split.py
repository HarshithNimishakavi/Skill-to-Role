import pandas as pd
from sklearn.model_selection import train_test_split
a=pd.read_csv("data/student_dataset.csv")
#dropping the unwanted columns
a=a.drop(columns=["student_id"])
#splitting the input and output features
x=a.iloc[:,:-1]
y=a['career_role']
#splitting into training and testing sets
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42,stratify=y)   

print("TRAINING DATA SHAPE")
print(x_train.shape)

print("\nTESTING DATA SHAPE")
print(x_test.shape)

print("\nTRAINING TARGET DISTRIBUTION")
print(y_train.value_counts())

print("\nTESTING TARGET DISTRIBUTION")
print(y_test.value_counts())