import sys
import os

# ============================================================
# ALLOW IMPORTING FROM PROJECT ROOT
# ============================================================

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# FILE PATHS
# ============================================================

DATA_FILE = "data/student_dataset_25features.csv"

MODEL_FILE = "models/svm_career_pipeline.pkl"


# ============================================================
# FEATURE COLUMNS
# ============================================================

FEATURE_COLUMNS = [
    "age",
    "year_of_study",
    "cgpa",

    "python_skill",
    "sql_skill",
    "ml_skill",
    "data_analysis_skill",
    "web_development_skill",
    "cybersecurity_skill",
    "dsa_skill",

    "communication_skill",
    "teamwork_skill",
    "problem_solving_skill",
    "adaptability_skill",

    "aptitude_score",
    "reasoning_score",

    "python_test_score",
    "sql_test_score",
    "ml_test_score",

    "interest_ai_ml",
    "interest_data_science",
    "interest_software",
    "interest_web",
    "interest_cybersecurity",

    "overall_assessment_score"
]


# ============================================================
# TARGET
# ============================================================

TARGET_COLUMN = "career_role"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("SKILL TO ROLE - FINAL SVM TRAINING")
print("=" * 60)

df = pd.read_csv(DATA_FILE)

print("\nDataset shape:")
print(df.shape)


# ============================================================
# CHECK FEATURES
# ============================================================

missing_features = [
    feature
    for feature in FEATURE_COLUMNS
    if feature not in df.columns
]

if missing_features:

    print("\nERROR: Missing features:")
    print(missing_features)

    sys.exit()


# ============================================================
# CREATE X AND y
# ============================================================

X = df[FEATURE_COLUMNS]

y = df[TARGET_COLUMN]


print("\nNumber of input features:")
print(X.shape[1])

print("\nNumber of samples:")
print(X.shape[0])

print("\nTarget classes:")
print(y.unique())


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print("\nTraining samples:")
print(X_train.shape[0])

print("Testing samples:")
print(X_test.shape[0])


# ============================================================
# CREATE SVM PIPELINE
# ============================================================

svm_pipeline = Pipeline([

    (
        "scaler",
        StandardScaler()
    ),

    (
        "svm",
        SVC(
            kernel="linear",
            C=0.1
        )
    )
])


# ============================================================
# TRAIN MODEL
# ============================================================

print("\nTraining SVM...")

svm_pipeline.fit(
    X_train,
    y_train
)

print("Training completed.")


# ============================================================
# PREDICTION
# ============================================================

y_pred = svm_pipeline.predict(X_test)


# ============================================================
# ACCURACY
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(
    f"\nSVM Accuracy: {accuracy * 100:.2f}%"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")
print("-" * 60)

print(
    classification_report(
        y_test,
        y_pred
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print("\nConfusion Matrix:")
print("-" * 60)

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# ============================================================
# SAVE MODEL
# ============================================================

os.makedirs(
    "models",
    exist_ok=True
)

joblib.dump(
    svm_pipeline,
    MODEL_FILE
)


print("\n" + "=" * 60)

print("Model saved successfully:")

print(MODEL_FILE)

print("=" * 60)

print("\nFinal SVM training completed successfully.")