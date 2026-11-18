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


# ============================================================
# FILE PATHS
# ============================================================

INPUT_FILE = "data/student_dataset.csv"

OUTPUT_FILE = "data/student_dataset_25features.csv"


# ============================================================
# ORIGINAL 24 FEATURES
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
    "interest_cybersecurity"
]


# ============================================================
# TARGET COLUMN
# ============================================================

TARGET_COLUMN = "career_role"


# ============================================================
# CREATE OVERALL ASSESSMENT SCORE
# ============================================================

def calculate_overall_score(row):

    scores = [
        row["python_skill"],
        row["sql_skill"],
        row["ml_skill"],
        row["data_analysis_skill"],
        row["web_development_skill"],
        row["cybersecurity_skill"],
        row["dsa_skill"],

        row["communication_skill"],
        row["teamwork_skill"],
        row["problem_solving_skill"],
        row["adaptability_skill"],

        row["aptitude_score"],
        row["reasoning_score"],

        row["python_test_score"],
        row["sql_test_score"],
        row["ml_test_score"],

        row["interest_ai_ml"],
        row["interest_data_science"],
        row["interest_software"],
        row["interest_web"],
        row["interest_cybersecurity"]
    ]

    return round(sum(scores) / len(scores), 2)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SKILL TO ROLE - PREPARE 25-FEATURE DATASET")
    print("=" * 60)

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    df = pd.read_csv(INPUT_FILE)

    print("\nOriginal dataset shape:")
    print(df.shape)

    # --------------------------------------------------------
    # Check required columns
    # --------------------------------------------------------

    required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        print("\nERROR: Missing columns:")
        print(missing_columns)

        sys.exit()

    # --------------------------------------------------------
    # Calculate overall assessment score
    # --------------------------------------------------------

    df["overall_assessment_score"] = df.apply(
        calculate_overall_score,
        axis=1
    )

    # --------------------------------------------------------
    # New 25-feature list
    # --------------------------------------------------------

    FINAL_FEATURE_COLUMNS = FEATURE_COLUMNS + [
        "overall_assessment_score"
    ]

    # --------------------------------------------------------
    # Arrange columns
    # --------------------------------------------------------

    final_columns = (
        ["student_id"]
        + FINAL_FEATURE_COLUMNS
        + [TARGET_COLUMN]
    )

    df = df[final_columns]

    # --------------------------------------------------------
    # Save new dataset
    # --------------------------------------------------------

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # --------------------------------------------------------
    # Verification
    # --------------------------------------------------------

    print("\nNew dataset shape:")
    print(df.shape)

    print("\nNumber of model features:")
    print(len(FINAL_FEATURE_COLUMNS))

    print("\nFeature columns:")
    for i, column in enumerate(FINAL_FEATURE_COLUMNS, start=1):
        print(f"{i:2}. {column}")

    print("\nFirst 5 overall assessment scores:")
    print(
        df["overall_assessment_score"]
        .head()
        .tolist()
    )

    if len(FINAL_FEATURE_COLUMNS) == 25:

        print("\n✓ 25 features verified.")

    else:

        print(
            "\nWARNING: Expected 25 features, "
            f"but found {len(FINAL_FEATURE_COLUMNS)}."
        )

    print("\nSaved dataset:")
    print(OUTPUT_FILE)

    print("\nDataset preparation completed successfully.")