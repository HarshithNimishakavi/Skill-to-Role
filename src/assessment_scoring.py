import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.questions import (
    SKILL_ASSESSMENT,
    OBJECTIVE_ASSESSMENT,
    BEHAVIORAL_QUESTIONS,
    INTEREST_QUESTIONS
)


# ============================================================
# 1. SKILL LEVEL SCORING
# ============================================================

SKILL_LEVEL_SCORES = {
    "Beginner": 40,
    "Intermediate": 70,
    "Advanced": 90
}


def calculate_skill_scores(skill_answers):
    """
    Convert Beginner / Intermediate / Advanced
    selections into numerical skill scores.

    Example:
        Python = Intermediate
        SQL = Advanced

    Output:
        {
            "python_skill": 70,
            "sql_skill": 90
        }
    """

    skill_scores = {}

    for skill, selected_level in skill_answers.items():

        if skill not in SKILL_ASSESSMENT:
            raise ValueError(f"Unknown skill: {skill}")

        if selected_level not in SKILL_LEVEL_SCORES:
            raise ValueError(
                f"Invalid level '{selected_level}' for {skill}"
            )

        skill_scores[skill] = SKILL_LEVEL_SCORES[selected_level]

    return skill_scores


# ============================================================
# 2. OBJECTIVE TEST SCORING
# ============================================================

def calculate_objective_score(test_name, student_answers):
    """
    Calculate percentage score for one objective test.

    student_answers must contain the selected answers
    in the same order as the questions.

    Example:
        ["7.2 days", "15%", "24", "40 km/h", "8% increase"]
    """

    if test_name not in OBJECTIVE_ASSESSMENT:
        raise ValueError(f"Unknown objective test: {test_name}")

    questions = OBJECTIVE_ASSESSMENT[test_name]

    if len(student_answers) != len(questions):
        raise ValueError(
            f"{test_name} requires {len(questions)} answers, "
            f"but received {len(student_answers)}."
        )

    correct_answers = 0

    for question, student_answer in zip(
        questions,
        student_answers
    ):
        if student_answer == question["answer"]:
            correct_answers += 1

    score = (correct_answers / len(questions)) * 100

    return round(score, 2)


def calculate_all_objective_scores(objective_answers):
    """
    Calculate scores for all objective tests.

    Expected input:

    {
        "python_test": [...],
        "sql_test": [...],
        "ml_test": [...],
        "data_analysis_test": [...],
        "web_development_test": [...],
        "cybersecurity_test": [...],
        "dsa_test": [...],
        "aptitude_test": [...],
        "reasoning_test": [...]
    }

    Returns numerical scores.
    """

    objective_scores = {}

    for test_name, answers in objective_answers.items():

        objective_scores[test_name] = calculate_objective_score(
            test_name,
            answers
        )

    return objective_scores
# ============================================================
# 3. BEHAVIORAL ASSESSMENT SCORING
# ============================================================

def calculate_likert_score(answers):
    """
    Convert Likert answers into a 0-100 score.

    Scale:
        1 = Strongly Disagree
        2 = Disagree
        3 = Neutral
        4 = Agree
        5 = Strongly Agree
    """

    if not answers:
        raise ValueError("No answers provided.")

    for answer in answers:

        if answer not in [1, 2, 3, 4, 5]:
            raise ValueError(
                "Likert answers must be between 1 and 5."
            )

    average = sum(answers) / len(answers)

    score = ((average - 1) / 4) * 100

    return round(score, 2)


def calculate_behavioral_scores(behavioral_answers):
    """
    Calculate scores for:

    communication
    teamwork
    problem solving
    adaptability
    """

    behavioral_scores = {}

    for skill, answers in behavioral_answers.items():

        if skill not in BEHAVIORAL_QUESTIONS:
            raise ValueError(
                f"Unknown behavioral category: {skill}"
            )

        expected_questions = len(
            BEHAVIORAL_QUESTIONS[skill]
        )

        if len(answers) != expected_questions:
            raise ValueError(
                f"{skill} requires {expected_questions} answers."
            )

        behavioral_scores[skill] = calculate_likert_score(
            answers
        )

    return behavioral_scores


# ============================================================
# 4. CAREER INTEREST SCORING
# ============================================================

def calculate_interest_scores(interest_answers):
    """
    Calculate career-interest scores.

    Scale:
        1 = Not Interested
        2 = Slightly Interested
        3 = Neutral
        4 = Interested
        5 = Highly Interested
    """

    interest_scores = {}

    for interest, answers in interest_answers.items():

        if interest not in INTEREST_QUESTIONS:
            raise ValueError(
                f"Unknown interest category: {interest}"
            )

        expected_questions = len(
            INTEREST_QUESTIONS[interest]
        )

        if len(answers) != expected_questions:
            raise ValueError(
                f"{interest} requires {expected_questions} answers."
            )

        interest_scores[interest] = calculate_likert_score(
            answers
        )

    return interest_scores


# ============================================================
# 5. COMPLETE ASSESSMENT SCORING
# ============================================================

def calculate_assessment_scores(
    skill_answers,
    objective_answers,
    behavioral_answers,
    interest_answers
):
    """
    Calculate all assessment scores together.
    """

    skill_scores = calculate_skill_scores(
        skill_answers
    )

    objective_scores = calculate_all_objective_scores(
        objective_answers
    )

    behavioral_scores = calculate_behavioral_scores(
        behavioral_answers
    )

    interest_scores = calculate_interest_scores(
        interest_answers
    )

    # Combine everything into one dictionary
    final_scores = {}

    final_scores.update(skill_scores)
    final_scores.update(objective_scores)
    final_scores.update(behavioral_scores)
    final_scores.update(interest_scores)

    return final_scores


# ============================================================
# 6. TEST THE SCORING SYSTEM
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SKILL TO ROLE - ASSESSMENT SCORING TEST")
    print("=" * 60)


    # --------------------------------------------------------
    # SAMPLE SKILL ANSWERS
    # --------------------------------------------------------

    skill_answers = {

        "python_skill": "Intermediate",

        "sql_skill": "Advanced",

        "ml_skill": "Intermediate",

        "data_analysis_skill": "Intermediate",

        "web_development_skill": "Beginner",

        "cybersecurity_skill": "Beginner",

        "dsa_skill": "Intermediate"
    }


    # --------------------------------------------------------
    # SAMPLE OBJECTIVE ANSWERS
    # --------------------------------------------------------
    # These are deliberately sample answers for testing.
    # Later React will collect these from the student.
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # SAMPLE BEHAVIORAL ANSWERS
    # --------------------------------------------------------

    behavioral_answers = {

        "communication_skill": [
            4, 5, 4, 4, 5
        ],

        "teamwork_skill": [
            5, 4, 4, 5, 4
        ],

        "problem_solving_skill": [
            5, 4, 5, 4, 5
        ],

        "adaptability_skill": [
            4, 4, 5, 4, 5
        ]
    }


    # --------------------------------------------------------
    # SAMPLE INTEREST ANSWERS
    # --------------------------------------------------------

    interest_answers = {

        "interest_ai_ml": [
            5, 5, 4, 5, 5
        ],

        "interest_data_science": [
            4, 4, 5, 4, 4
        ],

        "interest_software": [
            4, 3, 4, 4, 3
        ],

        "interest_web": [
            2, 3, 2, 3, 2
        ],

        "interest_cybersecurity": [
            2, 2, 3, 2, 2
        ]
    }


    # --------------------------------------------------------
    # CALCULATE EVERYTHING
    # --------------------------------------------------------

    scores = calculate_assessment_scores(
        skill_answers,
        objective_answers,
        behavioral_answers,
        interest_answers
    )


    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    print("\nFINAL ASSESSMENT SCORES")
    print("-" * 60)

    for feature, score in scores.items():

        print(
            f"{feature:<30} : {score}"
        )

    print("-" * 60)

    print("\nAssessment scoring completed successfully.")