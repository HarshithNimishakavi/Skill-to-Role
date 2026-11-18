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

import joblib

from create_features import create_feature_vector


# ============================================================
# MODEL PATH
# ============================================================

MODEL_FILE = "models/svm_career_pipeline.pkl"


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

print("=" * 60)
print("SKILL TO ROLE - CAREER PREDICTION")
print("=" * 60)

print("\nLoading trained SVM model...")

model = joblib.load(MODEL_FILE)

print("Model loaded successfully.")


# ============================================================
# STUDENT BASIC INFORMATION
# ============================================================

age = 21

year_of_study = 4

cgpa = 8.5


# ============================================================
# SKILL ASSESSMENT ANSWERS
# ============================================================

skill_answers = {

    "python_skill": "Intermediate",

    "sql_skill": "Advanced",

    "ml_skill": "Intermediate",

    "data_analysis_skill": "Intermediate",

    "web_development_skill": "Beginner",

    "cybersecurity_skill": "Beginner",

    "dsa_skill": "Intermediate"
}


# ============================================================
# OBJECTIVE TEST ANSWERS
# ============================================================

objective_answers = {

    "python_test": [
        "[1, 2, 3, 4]",
        "[4, 8]",
        "[1, 2] [1, 2, 3]",
        "0",
        "20"
    ],

    "sql_test": [
        "SELECT department FROM employees GROUP BY department HAVING AVG(salary) > 60000;",
        "SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);",
        "SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);",
        "WHERE column IS NULL",
        "HAVING"
    ],

    "ml_test": [
        "To avoid data leakage from the test set",
        "80%",
        "75%",
        "Overfitting",
        "KNN is based on distance calculations"
    ],

    "data_analysis_test": [
        "df.isnull()",
        "groupby()",
        "Histogram",
        "To understand patterns, distributions and relationships in data",
        "merge()"
    ],

    "web_development_test": [
        "<a>",
        "color",
        "JSON.parse()",
        "To define a way for applications to communicate over HTTP",
        "POST"
    ],

    "cybersecurity_test": [
        "Phishing",
        "To create a one-way representation of the password",
        "SQL Injection",
        "Verifying the identity of a user",
        "Determining what an authenticated user is allowed to access"
    ],

    "dsa_test": [
        "Stack",
        "O(1)",
        "Inorder",
        "Dijkstra's algorithm",
        "O(log n)"
    ],

    "aptitude_test": [
        "7.2 days",
        "15%",
        "24",
        "40 km/h",
        "8% increase"
    ],

    "reasoning_test": [
        "48",
        "EPH",
        "Ravi knows Python",
        "159",
        "D"
    ]
}


# ============================================================
# BEHAVIORAL ASSESSMENT ANSWERS
# ============================================================

behavioral_answers = {

    "communication_skill": [
        4, 4, 5, 4, 4
    ],

    "teamwork_skill": [
        4, 4, 5, 4, 4
    ],

    "problem_solving_skill": [
        5, 4, 5, 4, 5
    ],

    "adaptability_skill": [
        4, 4, 5, 4, 4
    ]
}


# ============================================================
# CAREER INTEREST ANSWERS
# ============================================================

interest_answers = {

    "interest_ai_ml": [
        5, 5, 4, 5, 5
    ],

    "interest_data_science": [
        4, 4, 4, 4, 4
    ],

    "interest_software": [
        3, 3, 3, 4, 3
    ],

    "interest_web": [
        2, 2, 2, 2, 2
    ],

    "interest_cybersecurity": [
        2, 2, 2, 2, 1
    ]
}


# ============================================================
# CREATE 25 FEATURES
# ============================================================

feature_df = create_feature_vector(

    age=age,

    year_of_study=year_of_study,

    cgpa=cgpa,

    skill_answers=skill_answers,

    objective_answers=objective_answers,

    behavioral_answers=behavioral_answers,

    interest_answers=interest_answers
)


# ============================================================
# VERIFY FEATURE COUNT
# ============================================================

print("\nNumber of input features:")
print(len(feature_df.columns))


if len(feature_df.columns) != 25:

    raise ValueError(
        f"Expected 25 features, "
        f"but received {len(feature_df.columns)}"
    )


# ============================================================
# PREDICT CAREER
# ============================================================

prediction = model.predict(feature_df)

predicted_career = prediction[0]


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n" + "=" * 60)

print("CAREER PREDICTION")

print("=" * 60)

print(
    f"\nRecommended Career: {predicted_career}"
)

print("\nPrediction completed successfully.")

print("=" * 60)