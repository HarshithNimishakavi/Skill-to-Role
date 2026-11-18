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
# REQUIRED SKILL LEVELS FOR EACH CAREER
# ============================================================

CAREER_SKILL_REQUIREMENTS = {

    "Machine Learning Engineer": {

        "python_skill": 80,
        "sql_skill": 70,
        "ml_skill": 85,
        "data_analysis_skill": 70,
        "dsa_skill": 75,
        "problem_solving_skill": 75
    },

    "Data Scientist": {

        "python_skill": 75,
        "sql_skill": 75,
        "ml_skill": 80,
        "data_analysis_skill": 85,
        "problem_solving_skill": 75,
        "aptitude_score": 70
    },

    "Data Analyst": {

        "python_skill": 60,
        "sql_skill": 80,
        "data_analysis_skill": 85,
        "communication_skill": 75,
        "problem_solving_skill": 70,
        "aptitude_score": 70
    },

    "Software Developer": {

        "python_skill": 70,
        "dsa_skill": 85,
        "problem_solving_skill": 80,
        "communication_skill": 65,
        "adaptability_skill": 70
    },

    "Web Developer": {

        "python_skill": 55,
        "sql_skill": 60,
        "web_development_skill": 85,
        "dsa_skill": 65,
        "problem_solving_skill": 70
    },

    "Cybersecurity Analyst": {

        "cybersecurity_skill": 85,
        "python_skill": 65,
        "sql_skill": 65,
        "dsa_skill": 60,
        "problem_solving_skill": 80,
        "reasoning_score": 75
    }
}


# ============================================================
# LEARNING RECOMMENDATIONS
# ============================================================

LEARNING_RESOURCES = {

    "python_skill":
        "Improve Python programming, OOP, functions, modules and problem solving.",

    "sql_skill":
        "Practice SQL queries, joins, subqueries, aggregation and window functions.",

    "ml_skill":
        "Study supervised learning, preprocessing, model evaluation and ML algorithms.",

    "data_analysis_skill":
        "Improve Pandas, NumPy, data cleaning, EDA and data visualization.",

    "web_development_skill":
        "Learn HTML, CSS, JavaScript, APIs and basic frontend/backend development.",

    "cybersecurity_skill":
        "Learn networking, authentication, vulnerabilities, security tools and threat detection.",

    "dsa_skill":
        "Practice arrays, strings, linked lists, stacks, queues, trees, graphs and algorithms.",

    "communication_skill":
        "Practice technical communication, presentations and explaining technical concepts.",

    "problem_solving_skill":
        "Practice coding problems, logical problems and algorithmic thinking.",

    "adaptability_skill":
        "Work on learning new technologies and solving unfamiliar technical problems.",

    "aptitude_score":
        "Practice quantitative aptitude, percentages, averages, ratios, time and work.",

    "reasoning_score":
        "Practice logical reasoning, series, coding-decoding and analytical reasoning."
}


# ============================================================
# SKILL GAP FUNCTION
# ============================================================

def analyze_skill_gap(feature_df, predicted_career):

    if predicted_career not in CAREER_SKILL_REQUIREMENTS:

        raise ValueError(
            f"No skill requirements defined for {predicted_career}"
        )

    required_skills = CAREER_SKILL_REQUIREMENTS[
        predicted_career
    ]

    gaps = []

    for skill, required_score in required_skills.items():

        student_score = float(
            feature_df.iloc[0][skill]
        )

        gap = required_score - student_score

        if gap > 0:

            gaps.append({
                "skill": skill,
                "current_score": student_score,
                "required_score": required_score,
                "gap": round(gap, 2),
                "status": "Needs Improvement",
                "recommendation": LEARNING_RESOURCES.get(
                    skill,
                    "Improve this skill through practice and projects."
                )
            })

        else:

            gaps.append({
                "skill": skill,
                "current_score": student_score,
                "required_score": required_score,
                "gap": 0,
                "status": "Good",
                "recommendation": "Maintain and strengthen this skill."
            })

    # Largest gaps first
    gaps.sort(
        key=lambda x: x["gap"],
        reverse=True
    )

    return gaps


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SKILL TO ROLE - SKILL GAP ANALYSIS")
    print("=" * 60)


    # ========================================================
    # LOAD MODEL
    # ========================================================

    model = joblib.load(
        MODEL_FILE
    )


    # ========================================================
    # SAMPLE STUDENT INFORMATION
    # ========================================================

    age = 21
    year_of_study = 4
    cgpa = 8.5


    # ========================================================
    # SKILL ANSWERS
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
    # OBJECTIVE ANSWERS
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
    # BEHAVIORAL ANSWERS
    # ========================================================

    behavioral_answers = {

        "communication_skill": [4, 4, 5, 4, 4],

        "teamwork_skill": [4, 4, 5, 4, 4],

        "problem_solving_skill": [5, 4, 5, 4, 5],

        "adaptability_skill": [4, 4, 5, 4, 4]
    }


    # ========================================================
    # INTEREST ANSWERS
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
    # PREDICT CAREER
    # ========================================================

    prediction = model.predict(
        feature_df
    )

    predicted_career = prediction[0]


    print("\nPredicted Career:")
    print("----------------------------")
    print(predicted_career)


    # ========================================================
    # ANALYZE SKILL GAP
    # ========================================================

    gaps = analyze_skill_gap(
        feature_df,
        predicted_career
    )


    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    print("\nSKILL GAP ANALYSIS")
    print("=" * 60)

    for item in gaps:

        print(
            f"\nSkill: {item['skill']}"
        )

        print(
            f"Current Score : {item['current_score']}"
        )

        print(
            f"Required Score: {item['required_score']}"
        )

        print(
            f"Gap           : {item['gap']}"
        )

        print(
            f"Status        : {item['status']}"
        )

        print(
            f"Recommendation: {item['recommendation']}"
        )


    print("\n" + "=" * 60)
    print("Skill-gap analysis completed successfully.")
    print("=" * 60)