import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
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


# =========================================================
# TRAIN-TEST SPLIT
# =========================================================

x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# =========================================================
# SVM HYPERPARAMETER TUNING
# =========================================================

svm_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC())
])


svm_parameters = {
    "svm__kernel": ["linear", "rbf"],
    "svm__C": [0.1, 1, 10],
    "svm__gamma": ["scale", "auto"]
}


svm_grid = GridSearchCV(
    estimator=svm_pipeline,
    param_grid=svm_parameters,
    cv=5,
    scoring="accuracy",
    n_jobs=-1
)


print("\nTUNING SVM...")

svm_grid.fit(x_train, y_train)


print("\nBEST SVM PARAMETERS")
print(svm_grid.best_params_)

print("\nBEST SVM CROSS-VALIDATION SCORE")
print(svm_grid.best_score_)


# Test best SVM
svm_best = svm_grid.best_estimator_

svm_pred = svm_best.predict(x_test)

svm_accuracy = accuracy_score(y_test, svm_pred)

print("\nTUNED SVM TEST ACCURACY")
print(svm_accuracy)

print("\nTUNED SVM CLASSIFICATION REPORT")
print(classification_report(y_test, svm_pred))

print("\nTUNED SVM CONFUSION MATRIX")
print(confusion_matrix(y_test, svm_pred))


# =========================================================
# RANDOM FOREST HYPERPARAMETER TUNING
# =========================================================

rf = RandomForestClassifier(
    random_state=42
)


rf_parameters = {
    "n_estimators": [100, 200],
    "max_depth": [None, 10, 20],
    "min_samples_split": [2, 5]
}


rf_grid = GridSearchCV(
    estimator=rf,
    param_grid=rf_parameters,
    cv=5,
    scoring="accuracy",
    n_jobs=-1
)


print("\nTUNING RANDOM FOREST...")

rf_grid.fit(x_train, y_train)


print("\nBEST RANDOM FOREST PARAMETERS")
print(rf_grid.best_params_)

print("\nBEST RANDOM FOREST CROSS-VALIDATION SCORE")
print(rf_grid.best_score_)


# Test best Random Forest
rf_best = rf_grid.best_estimator_

rf_pred = rf_best.predict(x_test)

rf_accuracy = accuracy_score(y_test, rf_pred)

print("\nTUNED RANDOM FOREST TEST ACCURACY")
print(rf_accuracy)

print("\nTUNED RANDOM FOREST CLASSIFICATION REPORT")
print(classification_report(y_test, rf_pred))

print("\nTUNED RANDOM FOREST CONFUSION MATRIX")
print(confusion_matrix(y_test, rf_pred))


# =========================================================
# FINAL COMPARISON
# =========================================================

print("\n==============================")
print("TUNED MODEL COMPARISON")
print("==============================")

print("SVM Accuracy           :", svm_accuracy)
print("Random Forest Accuracy :", rf_accuracy)