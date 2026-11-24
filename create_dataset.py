import os
import numpy as np
import pandas as pd


# ============================================================
# SETTINGS
# ============================================================

SEED = 42

rng = np.random.default_rng(SEED)

OUTPUT_DIR = "data"

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "student_dataset.csv"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# BALANCED CLASS COUNTS
# ============================================================

CLASS_COUNTS = {

    "Machine Learning Engineer": 420,

    "Data Scientist": 420,

    "Data Analyst": 420,

    "Software Developer": 420,

    "Web Developer": 410,

    "Cybersecurity Analyst": 410,
}


# ============================================================
# ROLE PROFILES
#
# These are prototype synthetic distributions.
# They are NOT real-world industry thresholds.
# ============================================================

ROLE_PROFILES = {

    "Machine Learning Engineer": {

        "python": 78,
        "sql": 65,
        "ml": 82,
        "data": 68,
        "web": 30,
        "cyber": 30,
        "dsa": 75,

        "communication": 65,
        "teamwork": 65,
        "problem_solving": 82,
        "adaptability": 70,

        "aptitude": 72,
        "reasoning": 75,

        "interest_ai_ml": 82,
        "interest_data_science": 65,
        "interest_software": 45,
        "interest_web": 25,
        "interest_cybersecurity": 20,
    },


    "Data Scientist": {

        "python": 75,
        "sql": 78,
        "ml": 78,
        "data": 84,
        "web": 25,
        "cyber": 25,
        "dsa": 62,

        "communication": 68,
        "teamwork": 65,
        "problem_solving": 78,
        "adaptability": 72,

        "aptitude": 75,
        "reasoning": 72,

        "interest_ai_ml": 65,
        "interest_data_science": 85,
        "interest_software": 40,
        "interest_web": 20,
        "interest_cybersecurity": 15,
    },


    "Data Analyst": {

        "python": 62,
        "sql": 82,
        "ml": 45,
        "data": 84,
        "web": 20,
        "cyber": 20,
        "dsa": 55,

        "communication": 78,
        "teamwork": 70,
        "problem_solving": 72,
        "adaptability": 70,

        "aptitude": 78,
        "reasoning": 72,

        "interest_ai_ml": 35,
        "interest_data_science": 70,
        "interest_software": 45,
        "interest_web": 20,
        "interest_cybersecurity": 18,
    },


    "Software Developer": {

        "python": 72,
        "sql": 60,
        "ml": 35,
        "data": 40,
        "web": 68,
        "cyber": 25,
        "dsa": 85,

        "communication": 68,
        "teamwork": 75,
        "problem_solving": 84,
        "adaptability": 78,

        "aptitude": 80,
        "reasoning": 78,

        "interest_ai_ml": 25,
        "interest_data_science": 20,
        "interest_software": 82,
        "interest_web": 65,
        "interest_cybersecurity": 15,
    },


    "Web Developer": {

        "python": 58,
        "sql": 55,
        "ml": 25,
        "data": 35,
        "web": 88,
        "cyber": 20,
        "dsa": 58,

        "communication": 72,
        "teamwork": 72,
        "problem_solving": 72,
        "adaptability": 80,

        "aptitude": 68,
        "reasoning": 65,

        "interest_ai_ml": 20,
        "interest_data_science": 15,
        "interest_software": 65,
        "interest_web": 88,
        "interest_cybersecurity": 12,
    },


    "Cybersecurity Analyst": {

        "python": 58,
        "sql": 62,
        "ml": 30,
        "data": 45,
        "web": 25,
        "cyber": 88,
        "dsa": 65,

        "communication": 65,
        "teamwork": 68,
        "problem_solving": 82,
        "adaptability": 75,

        "aptitude": 75,
        "reasoning": 88,

        "interest_ai_ml": 20,
        "interest_data_science": 15,
        "interest_software": 25,
        "interest_web": 15,
        "interest_cybersecurity": 88,
    },
}


# ============================================================
# GENERATE DATA
# ============================================================

rows = []

student_id = 1


for role, count in CLASS_COUNTS.items():

    profile = ROLE_PROFILES[role]


    for _ in range(count):

        row = {}


        # ----------------------------------------------------
        # BASIC INFORMATION
        # ----------------------------------------------------

        row["student_id"] = student_id

        student_id += 1

        row["age"] = int(
            rng.integers(
                19,
                25
            )
        )

        row["year_of_study"] = int(
            rng.integers(
                2,
                5
            )
        )

        row["cgpa"] = round(
            np.clip(
                rng.normal(
                    7.8,
                    0.9
                ),
                5.0,
                10.0
            ),
            2
        )


        # ----------------------------------------------------
        # SELF-ASSESSED SKILLS
        # ----------------------------------------------------

        row["python_skill"] = np.clip(
            rng.normal(
                profile["python"],
                18
            ),
            0,
            100
        )

        row["sql_skill"] = np.clip(
            rng.normal(
                profile["sql"],
                18
            ),
            0,
            100
        )

        row["ml_skill"] = np.clip(
            rng.normal(
                profile["ml"],
                18
            ),
            0,
            100
        )

        row["data_analysis_skill"] = np.clip(
            rng.normal(
                profile["data"],
                18
            ),
            0,
            100
        )

        row["web_development_skill"] = np.clip(
            rng.normal(
                profile["web"],
                18
            ),
            0,
            100
        )

        row["cybersecurity_skill"] = np.clip(
            rng.normal(
                profile["cyber"],
                18
            ),
            0,
            100
        )

        row["dsa_skill"] = np.clip(
            rng.normal(
                profile["dsa"],
                18
            ),
            0,
            100
        )


        # ----------------------------------------------------
        # BEHAVIORAL SKILLS
        # ----------------------------------------------------

        row["communication_skill"] = np.clip(
            rng.normal(
                profile["communication"],
                18
            ),
            0,
            100
        )

        row["teamwork_skill"] = np.clip(
            rng.normal(
                profile["teamwork"],
                18
            ),
            0,
            100
        )

        row["problem_solving_skill"] = np.clip(
            rng.normal(
                profile["problem_solving"],
                18
            ),
            0,
            100
        )

        row["adaptability_skill"] = np.clip(
            rng.normal(
                profile["adaptability"],
                18
            ),
            0,
            100
        )


        # ----------------------------------------------------
        # OBJECTIVE TEST SCORES
        #
        # These are correlated with the corresponding
        # skills but contain noise so the dataset is
        # not perfectly separable.
        # ----------------------------------------------------

        row["python_test_score"] = np.clip(
            (
                0.68 * row["python_skill"]
                +
                0.12 * row["dsa_skill"]
                +
                rng.normal(
                    0,
                    16
                )
            ),
            0,
            100
        )


        row["sql_test_score"] = np.clip(
            (
                0.68 * row["sql_skill"]
                +
                0.12 * row["data_analysis_skill"]
                +
                rng.normal(
                    0,
                    16
                )
            ),
            0,
            100
        )


        row["ml_test_score"] = np.clip(
            (
                0.68 * row["ml_skill"]
                +
                0.12 * row["python_skill"]
                +
                rng.normal(
                    0,
                    16
                )
            ),
            0,
            100
        )


        row["data_analysis_test_score"] = np.clip(
            (
                0.68 * row["data_analysis_skill"]
                +
                0.12 * row["sql_skill"]
                +
                rng.normal(
                    0,
                    16
                )
            ),
            0,
            100
        )


        row["web_development_test_score"] = np.clip(
            (
                0.68 * row["web_development_skill"]
                +
                0.12 * row["python_skill"]
                +
                rng.normal(
                    0,
                    16
                )
            ),
            0,
            100
        )


        row["cybersecurity_test_score"] = np.clip(
            (
                0.68 * row["cybersecurity_skill"]
                +
                0.12 * row["reasoning"] 
                if "reasoning" in row
                else
                0.68 * row["cybersecurity_skill"]
                +
                0.12 * profile["reasoning"]
                +
                rng.normal(
                    0,
                    16
                )
            ),
            0,
            100
        )


        row["dsa_test_score"] = np.clip(
            (
                0.68 * row["dsa_skill"]
                +
                0.12 * row["problem_solving_skill"]
                +
                rng.normal(
                    0,
                    16
                )
            ),
            0,
            100
        )


        row["aptitude_score"] = np.clip(
            (
                0.72 * profile["aptitude"]
                +
                rng.normal(
                    0,
                    15
                )
            ),
            0,
            100
        )


        row["reasoning_score"] = np.clip(
            (
                0.72 * profile["reasoning"]
                +
                rng.normal(
                    0,
                    15
                )
            ),
            0,
            100
        )


        # ----------------------------------------------------
        # CAREER INTERESTS
        # ----------------------------------------------------

        row["interest_ai_ml"] = np.clip(
            rng.normal(
                profile["interest_ai_ml"],
                18
            ),
            0,
            100
        )


        row["interest_data_science"] = np.clip(
            rng.normal(
                profile["interest_data_science"],
                18
            ),
            0,
            100
        )


        row["interest_software"] = np.clip(
            rng.normal(
                profile["interest_software"],
                18
            ),
            0,
            100
        )


        row["interest_web"] = np.clip(
            rng.normal(
                profile["interest_web"],
                18
            ),
            0,
            100
        )


        row["interest_cybersecurity"] = np.clip(
            rng.normal(
                profile["interest_cybersecurity"],
                18
            ),
            0,
            100
        )


        # ----------------------------------------------------
        # TARGET
        # ----------------------------------------------------

        row["career_role"] = role


        rows.append(row)


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(
    rows
)


# ============================================================
# ROUND NUMERIC COLUMNS
# ============================================================

numeric_columns = df.select_dtypes(
    include=["float"]
).columns

df[numeric_columns] = df[
    numeric_columns
].round(2)


# ============================================================
# SHUFFLE
# ============================================================

df = df.sample(
    frac=1,
    random_state=42
).reset_index(
    drop=True
)


# ============================================================
# SAVE
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# VALIDATION
# ============================================================

print()
print("=" * 60)
print("DATASET CREATED SUCCESSFULLY")
print("=" * 60)

print(
    f"Rows    : {df.shape[0]}"
)

print(
    f"Columns : {df.shape[1]}"
)

print()

print(
    "Career distribution:"
)

print(
    df["career_role"].value_counts()
)

print()

print(
    "Missing values:"
)

print(
    df.isnull().sum().sum()
)

print()

print(
    "Duplicate rows:"
)

print(
    df.duplicated().sum()
)

print()

print(
    f"Saved to: {OUTPUT_FILE}"
)

print(
    "=" * 60
)