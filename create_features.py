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

from assessment_scoring import calculate_assessment_scores


# ============================================================
# FEATURE ORDER
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
# CREATE FEATURE VECTOR
# ============================================================

def create_feature_vector(
    age,
    year_of_study,
    cgpa,
    skill_answers,
    objective_answers,
    behavioral_answers,
    interest_answers
):

    # --------------------------------------------------------
    # Calculate assessment scores
    # --------------------------------------------------------

    assessment_scores = calculate_assessment_scores(
        skill_answers=skill_answers,
        objective_answers=objective_answers,
        behavioral_answers=behavioral_answers,
        interest_answers=interest_answers
    )

    # --------------------------------------------------------
    # Calculate overall assessment score
    # --------------------------------------------------------

    score_values = list(assessment_scores.values())

    overall_assessment_score = round(
        sum(score_values) / len(score_values),
        2
    )

    # --------------------------------------------------------
    # Create feature dictionary
    # --------------------------------------------------------

    features = {

        # Basic information
        "age": age,
        "year_of_study": year_of_study,
        "cgpa": cgpa,

        # Skill assessment
        "python_skill": assessment_scores["python_skill"],
        "sql_skill": assessment_scores["sql_skill"],
        "ml_skill": assessment_scores["ml_skill"],
        "data_analysis_skill": assessment_scores["data_analysis_skill"],
        "web_development_skill": assessment_scores["web_development_skill"],
        "cybersecurity_skill": assessment_scores["cybersecurity_skill"],
        "dsa_skill": assessment_scores["dsa_skill"],

        # Behavioral assessment
        "communication_skill": assessment_scores["communication_skill"],
        "teamwork_skill": assessment_scores["teamwork_skill"],
        "problem_solving_skill": assessment_scores["problem_solving_skill"],
        "adaptability_skill": assessment_scores["adaptability_skill"],

        # Aptitude and reasoning
        "aptitude_score": assessment_scores["aptitude_test"],
        "reasoning_score": assessment_scores["reasoning_test"],

        # Technical tests
        "python_test_score": assessment_scores["python_test"],
        "sql_test_score": assessment_scores["sql_test"],
        "ml_test_score": assessment_scores["ml_test"],

        # Career interests
        "interest_ai_ml": assessment_scores["interest_ai_ml"],
        "interest_data_science": assessment_scores["interest_data_science"],
        "interest_software": assessment_scores["interest_software"],
        "interest_web": assessment_scores["interest_web"],
        "interest_cybersecurity": assessment_scores["interest_cybersecurity"],

        # Overall assessment
        "overall_assessment_score": overall_assessment_score
    }

    # --------------------------------------------------------
    # Convert to DataFrame
    # --------------------------------------------------------

    feature_df = pd.DataFrame(
        [features],
        columns=FEATURE_COLUMNS
    )

    return feature_df


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SKILL TO ROLE - FEATURE CREATION TEST")
    print("=" * 60)

    # ========================================================
    # BASIC INFORMATION
    # ========================================================

    age = 21
    year_of_study = 4
    cgpa = 8.5

    # ========================================================
    # SKILL ASSESSMENT
    # ========================================================

    skill_answers = {
        "python_skill": "Intermediate",
        "sql_skill": "Advanced",
        "ml_skill": "Intermediate",
        "data_analysis_skill": "Intermediate",
        "web_development_skill": "Beginner",
        "cybersecurity_skill": "Beginner",
        "dsa_skill": "Intermediate"
    }

    # ========================================================
    # OBJECTIVE TEST ANSWERS
    # ========================================================

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

    # ========================================================
    # BEHAVIORAL ASSESSMENT
    # ========================================================

    behavioral_answers = {

        "communication_skill": [4, 4, 5, 4, 4],

        "teamwork_skill": [4, 4, 5, 4, 4],

        "problem_solving_skill": [5, 4, 5, 4, 5],

        "adaptability_skill": [4, 4, 5, 4, 4]
    }

    # ========================================================
    # INTEREST ASSESSMENT
    # ========================================================

    interest_answers = {

        "interest_ai_ml": [5, 5, 4, 5, 5],

        "interest_data_science": [4, 4, 4, 4, 4],

        "interest_software": [3, 3, 3, 4, 3],

        "interest_web": [2, 2, 2, 2, 2],

        "interest_cybersecurity": [2, 2, 2, 2, 1]
    }

    # ========================================================
    # CREATE FEATURES
    # ========================================================

    feature_df = create_feature_vector(
        age=age,
        year_of_study=year_of_study,
        cgpa=cgpa,
        skill_answers=skill_answers,
        objective_answers=objective_answers,
        behavioral_answers=behavioral_answers,
        interest_answers=interest_answers
    )

    # ========================================================
    # DISPLAY FEATURES
    # ========================================================

    print("\nGENERATED FEATURES")
    print("-" * 60)

    print(feature_df.T)

    print("\nNumber of features:", len(feature_df.columns))

    # ========================================================
    # VERIFY
    # ========================================================

    if len(feature_df.columns) == 25:
        print("\n✓ Feature count verified: 25")
    else:
        print(
            "\nWARNING: Expected 25 features, "
            f"but received {len(feature_df.columns)}."
        )

    print("\nFeature creation completed successfully.")