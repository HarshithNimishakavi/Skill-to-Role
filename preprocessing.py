import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
# Load dataset
a = pd.read_csv("data/student_dataset.csv")

# Dropping unwanted columns
a = a.drop(columns=["student_id"])

# Splitting input and output features
x = a.iloc[:, :-1]
y = a["career_role"]

print("INPUT FEATURES SHAPE")
print(x.shape)

print("\nTARGET SHAPE")
print(y.shape)


# Splitting into training and testing sets
x_train, x_test, y_train, y_test = train_test_split( x,y,test_size=0.2,random_state=42,stratify=y)

# Standard Scaling
sc = StandardScaler()

# Fit scaler ONLY on training data
x_train = pd.DataFrame(sc.fit_transform(x_train),columns=x_train.columns)

# Transform testing data using the SAME scaler
x_test = pd.DataFrame(sc.transform(x_test),columns=x_test.columns)

# Display results
print("\nTRAINING DATA SHAPE")
print(x_train.shape)

print("\nTESTING DATA SHAPE")
print(x_test.shape)

print("\nTRAINING TARGET DISTRIBUTION")
print(y_train.value_counts())

print("\nTESTING TARGET DISTRIBUTION")
print(y_test.value_counts())

print("\nFIRST 5 SCALED TRAINING ROWS")
print(x_train.head())