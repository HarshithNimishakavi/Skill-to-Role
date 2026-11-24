import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# Load dataset
a = pd.read_csv("data/student_dataset.csv")

# Remove unwanted columns
a = a.drop(columns=["student_id"])

# Separate input and output
x = a.iloc[:, :-1]
y = a["career_role"]

print("INPUT FEATURES SHAPE")
print(x.shape)

print("\nTARGET SHAPE")
print(y.shape)


# Train-Test Split
x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Standard Scaling
sc = StandardScaler()

x_train = pd.DataFrame(
    sc.fit_transform(x_train),
    columns=x_train.columns
)

x_test = pd.DataFrame(
    sc.transform(x_test),
    columns=x_test.columns
)


# Create KNN model
knn = KNeighborsClassifier(n_neighbors=5)

# Train
knn.fit(x_train, y_train)

# Predict
y_pred = knn.predict(x_test)


# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nMODEL ACCURACY")
print(accuracy)

# Classification report
print("\nCLASSIFICATION REPORT")
print(classification_report(y_test, y_pred))

# Confusion matrix
print("\nCONFUSION MATRIX")
print(confusion_matrix(y_test, y_pred))