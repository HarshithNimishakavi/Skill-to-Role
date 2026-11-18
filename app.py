import os
import sys
import json
import hashlib
import hmac
import secrets
import joblib
import pandas as pd
import streamlit as st


# ============================================================
# PATH SETUP
# ============================================================

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


# ============================================================
# IMPORTS
# ============================================================

from data.questions import (
    SKILL_ASSESSMENT,
    OBJECTIVE_ASSESSMENT,
    BEHAVIORAL_QUESTIONS,
    INTEREST_QUESTIONS,
)

from src.skill_gap_analysis import CAREER_SKILL_REQUIREMENTS


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Skill to Role",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "logged_in": False,
    "user_email": "",
    "user_name": "",
    "show_dashboard": True,
    "create_account_mode": False,
    "objective_submitted": set(),
    "objective_submitted_levels": set(),
    "objective_active_section": "",
    "objective_level_by_section": {},
    "current_stage": 0,
    "completed_stages": set(),
    "answers": {},
    "analysis_result": None,
    "demo_loaded": False,
    "active_demo": None,
    "prediction_confidence": None,
    "assignment_history": [],
    "show_assignment_history": False,
    "show_assignment_history_page": False,
}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        if isinstance(value, set):
            st.session_state[key] = set(value)

        elif isinstance(value, dict):
            st.session_state[key] = {}

        elif isinstance(value, set):
            st.session_state[key] = set()

        else:
            st.session_state[key] = value


# ============================================================
# CONSTANTS
# ============================================================

DEMO_EMAIL = "demo@skilltorole.com"
DEMO_PASSWORD = "skill123"
ACCOUNT_STORE_PATH = os.path.join(ROOT_DIR, "data", "accounts.json")

OBJECTIVE_SCORE_KEYS = {
    "python_test": "python_test_score",
    "sql_test": "sql_test_score",
    "ml_test": "ml_test_score",
    "aptitude_test": "aptitude_score",
    "reasoning_test": "reasoning_score",
}
for objective_section_name in OBJECTIVE_ASSESSMENT:
    OBJECTIVE_SCORE_KEYS.setdefault(
        objective_section_name,
        f"{objective_section_name}_score",
    )

STAGES = [
    "Academic Information",
    "Skill Assessment",
    "Objective Assessment",
    "Behavioral Assessment",
    "Career Interests",
    "Career Prediction",
    "Skill Gap Analysis",
    "Personalized Roadmap",
]

STAGE_ICONS = [
    "🎓",
    "🧠",
    "📝",
    "🤝",
    "❤️",
    "🎯",
    "📊",
    "🗺️",
]

MODEL_PATH = os.path.join(
    ROOT_DIR,
    "models",
    "svm_career_pipeline.pkl"
)


# ============================================================
# MODEL FEATURES
# ============================================================

MODEL_FEATURE_COLUMNS = [

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

    "overall_assessment_score",
]


# ============================================================
# CAREER CRITERIA
# ============================================================

CAREER_CRITERIA_WEIGHTS = {

    "Machine Learning Engineer": {

        "Python": 20,
        "Machine Learning": 25,
        "DSA": 15,
        "Data Analysis": 10,
        "SQL": 10,
        "Problem Solving": 10,
        "AI/ML Interest": 10,
    },

    "Data Scientist": {

        "Python": 15,
        "Machine Learning": 20,
        "Data Analysis": 20,
        "SQL": 15,
        "Problem Solving": 10,
        "Data Science Interest": 10,
        "Reasoning": 5,
        "Aptitude": 5,
    },

    "Data Analyst": {

        "SQL": 20,
        "Data Analysis": 25,
        "Python": 10,
        "Aptitude": 10,
        "Reasoning": 10,
        "Communication": 10,
        "Data Science Interest": 10,
        "Problem Solving": 5,
    },

    "Software Developer": {

        "DSA": 25,
        "Python": 15,
        "Web Development": 15,
        "SQL": 10,
        "Problem Solving": 15,
        "Communication": 5,
        "Software Interest": 10,
        "Adaptability": 5,
    },

    "Web Developer": {

        "Web Development": 30,
        "Python": 10,
        "SQL": 10,
        "DSA": 10,
        "Problem Solving": 10,
        "Communication": 10,
        "Web Interest": 15,
        "Adaptability": 5,
    },

    "Cybersecurity Analyst": {

        "Cybersecurity": 30,
        "Reasoning": 15,
        "Problem Solving": 15,
        "Python": 10,
        "SQL": 10,
        "DSA": 10,
        "Cybersecurity Interest": 10,
    },
}


# ============================================================
# TECHNICAL SCORE MAP
# ============================================================

TECHNICAL_SCORE_MAP = {

    "Python": (
        "python_skill",
        "python_test_score"
    ),

    "SQL": (
        "sql_skill",
        "sql_test_score"
    ),

    "Machine Learning": (
        "ml_skill",
        "ml_test_score"
    ),

    "Data Analysis": (
        "data_analysis_skill",
        None
    ),

    "Web Development": (
        "web_development_skill",
        None
    ),

    "Cybersecurity": (
        "cybersecurity_skill",
        None
    ),

    "DSA": (
        "dsa_skill",
        None
    ),
}


# ============================================================
# DEMO PROFILES
# ============================================================

DEMO_PROFILES = {

    "AI / ML Profile": {

        "age": 21,
        "year": 4,
        "cgpa": 8.7,

        "skills": {

            "python": "Advanced",
            "sql": "Intermediate",
            "ml": "Advanced",
            "data_analysis": "Advanced",
            "web_development": "Beginner",
            "cybersecurity": "Beginner",
            "dsa": "Intermediate",
        },

        "objective_scores": {

            "python_test_score": 100,
            "sql_test_score": 90,
            "ml_test_score": 100,
            "aptitude_score": 80,
            "reasoning_score": 85,
        },

        "behavioral": {

            "communication_skill": 4,
            "teamwork_skill": 4,
            "problem_solving_skill": 5,
            "adaptability_skill": 4,
        },

        "interests": {

            "interest_ai_ml": 5,
            "interest_data_science": 4,
            "interest_software": 3,
            "interest_web": 2,
            "interest_cybersecurity": 2,
        },
    },

    "Data Science Profile": {

        "age": 21,
        "year": 4,
        "cgpa": 8.5,

        "skills": {

            "python": "Advanced",
            "sql": "Advanced",
            "ml": "Intermediate",
            "data_analysis": "Advanced",
            "web_development": "Beginner",
            "cybersecurity": "Beginner",
            "dsa": "Intermediate",
        },

        "objective_scores": {

            "python_test_score": 95,
            "sql_test_score": 100,
            "ml_test_score": 85,
            "aptitude_score": 90,
            "reasoning_score": 90,
        },

        "behavioral": {

            "communication_skill": 5,
            "teamwork_skill": 4,
            "problem_solving_skill": 4,
            "adaptability_skill": 4,
        },

        "interests": {

            "interest_ai_ml": 4,
            "interest_data_science": 5,
            "interest_software": 3,
            "interest_web": 2,
            "interest_cybersecurity": 2,
        },
    },

    "Software Developer Profile": {

        "age": 21,
        "year": 4,
        "cgpa": 8.2,

        "skills": {

            "python": "Intermediate",
            "sql": "Intermediate",
            "ml": "Beginner",
            "data_analysis": "Beginner",
            "web_development": "Intermediate",
            "cybersecurity": "Beginner",
            "dsa": "Advanced",
        },

        "objective_scores": {

            "python_test_score": 85,
            "sql_test_score": 80,
            "ml_test_score": 60,
            "aptitude_score": 90,
            "reasoning_score": 90,
        },

        "behavioral": {

            "communication_skill": 4,
            "teamwork_skill": 5,
            "problem_solving_skill": 5,
            "adaptability_skill": 4,
        },

        "interests": {

            "interest_ai_ml": 2,
            "interest_data_science": 2,
            "interest_software": 5,
            "interest_web": 4,
            "interest_cybersecurity": 2,
        },
    },

    "Web Developer Profile": {

        "age": 21,
        "year": 4,
        "cgpa": 8.0,

        "skills": {

            "python": "Intermediate",
            "sql": "Intermediate",
            "ml": "Beginner",
            "data_analysis": "Beginner",
            "web_development": "Advanced",
            "cybersecurity": "Beginner",
            "dsa": "Intermediate",
        },

        "objective_scores": {

            "python_test_score": 75,
            "sql_test_score": 70,
            "ml_test_score": 50,
            "aptitude_score": 75,
            "reasoning_score": 70,
        },

        "behavioral": {

            "communication_skill": 4,
            "teamwork_skill": 5,
            "problem_solving_skill": 4,
            "adaptability_skill": 5,
        },

        "interests": {

            "interest_ai_ml": 2,
            "interest_data_science": 2,
            "interest_software": 4,
            "interest_web": 5,
            "interest_cybersecurity": 1,
        },
    },
}


# ============================================================
# LEARNING RESOURCES
# ============================================================

LEARNING_RESOURCES = {

    "Python": {

        "description":
            "Build strong Python programming fundamentals required for AI, ML and software development.",

        "topics": [
            "Variables and Data Types",
            "Conditional Statements",
            "For and While Loops",
            "Lists, Tuples, Sets and Dictionaries",
            "Functions",
            "Lambda Functions",
            "List and Dictionary Comprehensions",
            "Exception Handling",
            "File Handling",
            "Modules and Packages",
            "Object-Oriented Programming",
            "NumPy",
            "Pandas",
            "Decorators",
            "Generators",
            "Iterators",
            "Context Managers",
            "Efficient Data Structures",
        ],

        "order": [
            "Python Fundamentals",
            "Functions and Collections",
            "Object-Oriented Programming",
            "NumPy and Pandas",
            "Advanced Python",
            "Projects",
        ],

        "link":
            "https://www.youtube.com/@coreyms",
    },

    "SQL": {

        "description":
            "Learn SQL for databases, data analysis and technical interviews.",

        "topics": [
            "SELECT and FROM",
            "WHERE Conditions",
            "ORDER BY",
            "DISTINCT",
            "COUNT, SUM and AVG",
            "GROUP BY",
            "HAVING",
            "INNER JOIN",
            "LEFT JOIN",
            "RIGHT JOIN",
            "Subqueries",
            "CASE Statements",
            "Common Table Expressions",
            "Window Functions",
            "Query Optimization",
            "Indexes",
            "Execution Plans",
        ],

        "order": [
            "SQL Basics",
            "Filtering and Aggregation",
            "Joins",
            "Subqueries",
            "CTEs",
            "Window Functions",
            "Advanced SQL Practice",
        ],

        "link":
            "https://www.youtube.com/channel/UC7cs8q-gJRlGwj4A8OmCmXg",
    },

    "Machine Learning": {

        "description":
            "Learn the complete machine learning workflow from data preprocessing to model deployment.",

        "topics": [
            "What Machine Learning Is",
            "Supervised Learning",
            "Unsupervised Learning",
            "Classification",
            "Regression",
            "Train-Test Split",
            "Data Preprocessing",
            "Feature Engineering",
            "Linear Regression",
            "Logistic Regression",
            "KNN",
            "Decision Trees",
            "Random Forest",
            "SVM",
            "Naive Bayes",
            "Confusion Matrix",
            "Precision",
            "Recall",
            "F1 Score",
            "Cross Validation",
            "Hyperparameter Tuning",
            "ML Pipelines",
            "Model Deployment",
        ],

        "order": [
            "ML Fundamentals",
            "Data Preprocessing",
            "Supervised Learning",
            "Unsupervised Learning",
            "Model Evaluation",
            "Hyperparameter Tuning",
            "Projects",
            "Deployment",
        ],

        "link":
            "https://www.youtube.com/@statquest",
    },

    "Data Analysis": {

        "description":
            "Develop practical skills for cleaning, exploring and visualizing data.",

        "topics": [
            "Excel Basics",
            "Data Cleaning",
            "Missing Values",
            "Duplicate Handling",
            "NumPy",
            "Pandas",
            "Exploratory Data Analysis",
            "Grouping and Aggregation",
            "Matplotlib",
            "Seaborn",
            "Correlation",
            "Outlier Detection",
            "Feature Analysis",
            "Finding Patterns",
            "Dashboard Development",
        ],

        "order": [
            "Excel",
            "NumPy",
            "Pandas",
            "Data Cleaning",
            "EDA",
            "Visualization",
            "Dashboard Development",
        ],

        "link":
            "https://www.youtube.com/channel/UC7cs8q-gJRlGwj4A8OmCmXg",
    },

    "DSA": {

        "description":
            "Build problem-solving skills required for software and technical interviews.",

        "topics": [
            "Time Complexity",
            "Space Complexity",
            "Arrays",
            "Strings",
            "Hashing",
            "Two Pointers",
            "Sliding Window",
            "Linked Lists",
            "Stacks",
            "Queues",
            "Binary Search",
            "Recursion",
            "Trees",
            "Binary Search Trees",
            "Heaps",
            "Graphs",
            "Dynamic Programming",
        ],

        "order": [
            "Arrays and Strings",
            "Hashing",
            "Linked Lists",
            "Stacks and Queues",
            "Binary Search",
            "Trees",
            "Graphs",
            "Dynamic Programming",
        ],

        "link":
            "https://takeuforward.org/dsa/strivers-a2z-sheet-learn-dsa-a-to-z",
    },

    "Web Development": {

        "description":
            "Learn the fundamentals required to build modern web applications.",

        "topics": [
            "HTML",
            "CSS",
            "Responsive Design",
            "JavaScript",
            "DOM",
            "Events",
            "ES6",
            "APIs",
            "Git and GitHub",
            "React",
            "Backend Fundamentals",
            "Databases",
            "REST APIs",
            "Deployment",
        ],

        "order": [
            "HTML and CSS",
            "JavaScript",
            "DOM and APIs",
            "Git and GitHub",
            "React",
            "Backend",
            "Database",
            "Deployment",
        ],

        "link":
            "https://www.youtube.com/@freecodecamp",
    },

    "Cybersecurity": {

        "description":
            "Build foundational knowledge of networks, systems and cybersecurity.",

        "topics": [
            "Computer Networking",
            "TCP/IP",
            "DNS",
            "HTTP and HTTPS",
            "Linux Basics",
            "Authentication",
            "Authorization",
            "Common Vulnerabilities",
            "Phishing",
            "Malware",
            "Web Security",
            "Network Security",
            "Wireshark",
            "Security Monitoring",
        ],

        "order": [
            "Networking",
            "Linux",
            "Security Fundamentals",
            "Web Security",
            "Network Security",
            "Security Tools",
        ],

        "link":
            "https://www.youtube.com/@networkchuck",
    },
}


# ============================================================
# ROADMAP
# ============================================================

def get_roadmap(career):

    if not career:
        return []

    career_lower = career.lower()

    if "machine learning" in career_lower:

        return [
            (
                "Python",
                "Strengthen Python, OOP, NumPy and Pandas",
                "Python"
            ),
            (
                "SQL",
                "Practice joins, subqueries and window functions",
                "SQL"
            ),
            (
                "Machine Learning",
                "Master preprocessing, ML algorithms and evaluation",
                "Machine Learning"
            ),
            (
                "Data Analysis",
                "Practice EDA, visualization and preprocessing",
                "Data Analysis"
            ),
            (
                "DSA",
                "Practice arrays, strings, trees and graphs",
                "DSA"
            ),
            (
                "Projects",
                "Build 2–3 complete machine learning projects",
                None
            ),
            (
                "Deployment",
                "Learn Streamlit, APIs and model deployment",
                None
            ),
        ]

    if "data scientist" in career_lower:

        return [
            (
                "Python",
                "Strengthen NumPy, Pandas and Python",
                "Python"
            ),
            (
                "SQL",
                "Master joins, CTEs and window functions",
                "SQL"
            ),
            (
                "Data Analysis",
                "Practice EDA and visualization",
                "Data Analysis"
            ),
            (
                "Machine Learning",
                "Learn supervised and unsupervised learning",
                "Machine Learning"
            ),
            (
                "Projects",
                "Build practical data science projects",
                None
            ),
            (
                "Communication",
                "Practice explaining data insights clearly",
                None
            ),
        ]

    if "data analyst" in career_lower:

        return [
            (
                "SQL",
                "Master joins, subqueries and window functions",
                "SQL"
            ),
            (
                "Excel",
                "Practice Pivot Tables, XLOOKUP and dashboards",
                None
            ),
            (
                "Data Analysis",
                "Learn data cleaning, EDA and visualization",
                "Data Analysis"
            ),
            (
                "Power BI",
                "Build interactive dashboards",
                None
            ),
            (
                "Statistics",
                "Learn practical descriptive statistics",
                None
            ),
            (
                "Projects",
                "Create portfolio-ready analytics dashboards",
                None
            ),
        ]

    if "software developer" in career_lower:

        return [
            (
                "Python",
                "Strengthen programming and OOP",
                "Python"
            ),
            (
                "DSA",
                "Practice arrays, strings, trees and graphs",
                "DSA"
            ),
            (
                "SQL",
                "Learn relational databases",
                "SQL"
            ),
            (
                "Git",
                "Learn Git and GitHub workflows",
                None
            ),
            (
                "Development",
                "Build real-world software applications",
                None
            ),
            (
                "Projects",
                "Create 2–3 strong portfolio projects",
                None
            ),
        ]

    if "web developer" in career_lower:

        return [
            (
                "HTML & CSS",
                "Build responsive web pages",
                "Web Development"
            ),
            (
                "JavaScript",
                "Learn DOM, events and APIs",
                "Web Development"
            ),
            (
                "Frontend",
                "Learn React fundamentals",
                "Web Development"
            ),
            (
                "Backend",
                "Learn APIs and backend development",
                "Web Development"
            ),
            (
                "Database",
                "Learn SQL and database integration",
                "SQL"
            ),
            (
                "Projects",
                "Build complete web applications",
                None
            ),
        ]

    if "cybersecurity" in career_lower:

        return [
            (
                "Networking",
                "Learn TCP/IP, DNS, HTTP and common protocols",
                "Cybersecurity"
            ),
            (
                "Linux",
                "Practice Linux commands and administration",
                "Cybersecurity"
            ),
            (
                "Cybersecurity",
                "Learn common attacks and vulnerabilities",
                "Cybersecurity"
            ),
            (
                "Python",
                "Use Python for security automation",
                "Python"
            ),
            (
                "Security Tools",
                "Practice networking and security tools",
                "Cybersecurity"
            ),
            (
                "Projects",
                "Build practical cybersecurity projects",
                None
            ),
        ]

    return [
        (
            "Core Skills",
            "Strengthen the most important skills for your role",
            None
        ),
        (
            "Projects",
            "Build practical portfolio projects",
            None
        ),
        (
            "Problem Solving",
            "Practice technical problem solving",
            None
        ),
        (
            "Interview Preparation",
            "Prepare technical and HR questions",
            None
        ),
    ]


# ============================================================
def roadmap_topic_is_lacking(resource, topic, answers, submitted_sections, skill_gap, self_skills):
    section_by_resource = {
        "Python": "python_test",
        "SQL": "sql_test",
        "Machine Learning": "ml_test",
        "Data Analysis": "data_analysis_test",
        "Web Development": "web_development_test",
        "Cybersecurity": "cybersecurity_test",
        "DSA": "dsa_test",
    }
    topic_groups = {
        "Python": [
            ("Lists", ("list", "collection", "comprehension", "set")),
            ("Tuples", ("tuple",)),
            ("Dictionaries", ("dictionary", "dict")),
            ("Conditionals", ("conditional", "if/else", "if else", "branch")),
            ("Loops", ("loop", "iteration", "for and while")),
        ],
        "SQL": [
            ("SELECT and filtering", ("select", "where", "filter")),
            ("Aggregation", ("count", "sum", "avg", "group", "having", "aggregation")),
            ("Joins", ("join",)),
            ("Subqueries", ("subquer", "nested quer")),
            ("NULL and ordering", ("null", "order", "distinct")),
        ],
        "Machine Learning": [
            ("Learning types", ("learning", "classification", "regression")),
            ("Preprocessing", ("preprocess", "train-test", "feature engineering")),
            ("Evaluation", ("evaluation", "precision", "recall", "confusion", "f1")),
            ("Overfitting", ("overfit", "regularization", "cross validation", "hyperparameter")),
            ("Features and scaling", ("feature", "scaling", "knn")),
        ],
        "Data Analysis": [
            ("Missing values", ("missing", "cleaning", "duplicate")),
            ("Grouping and aggregation", ("group", "aggregat")),
            ("Combining data", ("merge", "combine", "concat")),
            ("Exploratory analysis", ("exploratory", "eda", "pattern", "correlation")),
            ("Charts and distributions", ("chart", "visual", "matplotlib", "seaborn", "distribution")),
        ],
        "Web Development": [
            ("HTML structure", ("html", "element", "hyperlink")),
            ("Forms and semantics", ("form", "label", "semantic", "input")),
            ("CSS layout", ("css", "responsive", "layout", "style")),
            ("JavaScript", ("javascript", "dom", "event", "es6", "react")),
            ("HTTP and accessibility", ("http", "api", "accessib", "rest")),
        ],
        "Cybersecurity": [
            ("Phishing and social engineering", ("phish", "social engineering")),
            ("Authentication and authorization", ("authentication", "authorization", "access control")),
            ("Passwords and hashing", ("password", "hash")),
            ("Web and database security", ("sql", "injection", "web security", "vulnerab")),
            ("Network and incident response", ("network", "tcp/ip", "dns", "http", "incident", "monitoring", "firewall")),
        ],
        "DSA": [
            ("Arrays and hashing", ("array", "string", "hash", "two pointer", "sliding window")),
            ("Stacks and queues", ("stack", "queue")),
            ("Sorting and searching", ("sort", "search", "binary search")),
            ("Trees", ("tree", "heap")),
            ("Graphs and complexity", ("graph", "complexity", "dynamic programming", "recursion")),
        ],
    }
    section_name = section_by_resource.get(resource)
    if section_name is None:
        return False

    normalized_topic = " ".join(str(topic).lower().split())
    categories = [
        category
        for category, keywords in topic_groups.get(resource, [])
        if any(keyword in normalized_topic for keyword in keywords)
    ]
    objective_lacking = False
    if categories and section_name in submitted_sections:
        questions = OBJECTIVE_ASSESSMENT.get(section_name, [])
        student_answers = answers.get(section_name, [])
        category_questions = [
            (index, question)
            for index, question in enumerate(questions)
            if question.get("topic") in categories
        ]
        objective_lacking = any(
            index >= len(student_answers)
            or student_answers[index] != question.get("answer")
            for index, question in category_questions
        )
    if objective_lacking:
        return True

    skill_key_by_resource = {
        "Python": "python_skill",
        "SQL": "sql_skill",
        "Machine Learning": "ml_skill",
        "Data Analysis": "data_analysis_skill",
        "Web Development": "web_development_skill",
        "Cybersecurity": "cybersecurity_skill",
        "DSA": "dsa_skill",
    }
    skill_key = skill_key_by_resource.get(resource)
    skill_level = self_skills.get(skill_key.replace("_skill", ""), "Beginner") if skill_key else "Beginner"
    level_order = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}

    def normalize_terms(value):
        terms = " ".join(str(value).lower().replace("/", " ").split())
        terms = terms.replace("conditional", "condition").replace("conditions", "condition")
        terms = terms.replace("dictionaries", "dictionary").replace("tuples", "tuple")
        terms = terms.replace("lists", "list").replace("loops", "loop")
        return {
            term for term in terms.split()
            if term not in {"and", "or", "the", "of", "with", "basic", "basics", "concepts"}
        }

    skill_assessment = SKILL_ASSESSMENT.get(skill_key, {}) if skill_key else {}
    level_topics = skill_assessment.get("levels", {})
    resource_terms = normalize_terms(topic)
    best_level = None
    best_similarity = 0.0
    for level_name, assessment_topics in level_topics.items():
        for assessment_topic in assessment_topics:
            assessment_terms = normalize_terms(assessment_topic)
            if not resource_terms or not assessment_terms:
                continue
            overlap = len(resource_terms & assessment_terms)
            similarity = overlap / min(len(resource_terms), len(assessment_terms))
            if similarity > best_similarity:
                best_similarity = similarity
                best_level = level_name

    if best_level and best_similarity >= 0.5:
        return level_order.get(skill_level, 0) < level_order.get(best_level, 0)
    return False


# MODEL LOADING
# ============================================================

@st.cache_resource
def load_model():

    if not os.path.exists(MODEL_PATH):
        return None

    try:
        return joblib.load(MODEL_PATH)

    except Exception:
        return None


# ============================================================
# SCORE FUNCTIONS
# ============================================================

def skill_to_score(level):

    return {

        "Beginner": 40,
        "Intermediate": 70,
        "Advanced": 90,

    }.get(
        level,
        40
    )


def likert_to_score(value):

    return {

        1: 0,
        2: 25,
        3: 50,
        4: 75,
        5: 100,

    }.get(
        value,
        0
    )


# ============================================================
# DEMO ANSWER GENERATOR
# ============================================================

def create_demo_question_answers(
    questions,
    target_score
):

    if not questions:
        return []

    total = len(questions)

    correct_count = round(
        total * target_score / 100
    )

    correct_count = max(
        0,
        min(
            total,
            correct_count
        )
    )

    answers = []

    for index, question in enumerate(questions):

        correct_answer = question.get(
            "answer"
        )

        if index < correct_count:

            answers.append(
                correct_answer
            )

        else:

            options = question.get(
                "options",
                []
            )

            wrong_options = [
                option
                for option in options
                if option != correct_answer
            ]

            if wrong_options:

                answers.append(
                    wrong_options[0]
                )

            else:

                answers.append(
                    correct_answer
                )

    return answers


# ============================================================
# DEMO PROFILE LOADER
# ============================================================

def load_demo_profile(profile_name):

    profile = DEMO_PROFILES.get(
        profile_name
    )

    if not profile:
        return

    keys_to_clear = []

    for key in list(
        st.session_state.keys()
    ):

        key_string = str(key)

        prefixes = (
            "skill_slider_",
            "objective_",
            "behavior_",
            "interest_",
            "roadmap_topic_",
        )

        if key_string.startswith(
            prefixes
        ):

            keys_to_clear.append(
                key
            )

    for key in keys_to_clear:

        del st.session_state[key]

    st.session_state.academic_age = (
        profile["age"]
    )

    st.session_state.academic_year = (
        profile["year"]
    )

    st.session_state.academic_cgpa = (
        profile["cgpa"]
    )

    for skill_key, level in profile[
        "skills"
    ].items():

        st.session_state[
            f"skill_slider_value_{skill_key}"
        ] = [
            "Beginner",
            "Intermediate",
            "Advanced",
        ].index(level)

    objective_scores = profile[
        "objective_scores"
    ].copy()

    objective_answers = {}
    objective_answers_by_level = {}
    objective_scores_by_level = {}
    objective_submitted_levels = set()
    technical_skill_by_section = {
        "python_test": "python",
        "sql_test": "sql",
        "ml_test": "ml",
        "data_analysis_test": "data_analysis",
        "web_development_test": "web_development",
        "cybersecurity_test": "cybersecurity",
        "dsa_test": "dsa",
    }
    level_ranges = {
        "Beginner": (0, 5),
        "Intermediate": (2, 7),
        "Advanced": (5, 10),
    }

    for section_name, questions in (
        OBJECTIVE_ASSESSMENT.items()
    ):

        target_score = objective_scores.get(
            OBJECTIVE_SCORE_KEYS.get(section_name, ""),
            60
        )

        skill_key = technical_skill_by_section.get(section_name)
        skill_level = profile["skills"].get(skill_key, "Beginner") if skill_key else "General"
        levels_to_fill = ["Beginner", "Intermediate", "Advanced"] if skill_key else ["General"]
        objective_answers_by_level[section_name] = {}
        objective_scores_by_level[section_name] = {}
        for question_level in levels_to_fill:
            if skill_key:
                start_index, end_index = level_ranges[question_level]
                level_questions = questions[start_index:end_index]
            else:
                level_questions = questions
            level_answers = create_demo_question_answers(level_questions, target_score)
            objective_answers_by_level[section_name][question_level] = level_answers
            correct_count = sum(
                answer == question["answer"]
                for answer, question in zip(level_answers, level_questions)
            )
            objective_scores_by_level[section_name][question_level] = round(
                correct_count / len(level_questions) * 100, 2
            ) if level_questions else 0
            objective_submitted_levels.add((section_name, question_level))
            for index, answer in enumerate(level_answers):
                st.session_state[
                    f"objective_{section_name}_{question_level}_{index}"
                ] = answer
            if question_level == skill_level or (not skill_key and question_level == "General"):
                objective_answers[section_name] = level_answers
                score_key = OBJECTIVE_SCORE_KEYS.get(section_name)
                if score_key:
                    objective_scores[score_key] = objective_scores_by_level[section_name][question_level]

    behavioral_answers = {}

    behavioral_options = [

        "1 - Strongly Disagree",
        "2 - Disagree",
        "3 - Neutral",
        "4 - Agree",
        "5 - Strongly Agree",
    ]

    for key, questions in (
        BEHAVIORAL_QUESTIONS.items()
    ):

        value = profile[
            "behavioral"
        ].get(
            key,
            3
        )

        section_answers = []

        for index, question in enumerate(
            questions
        ):

            value = max(
                1,
                min(
                    5,
                    int(value)
                )
            )

            answer = behavioral_options[
                value - 1
            ]

            section_answers.append(
                value
            )

            st.session_state[
                f"behavior_{key}_{index}"
            ] = answer

        behavioral_answers[
            key
        ] = section_answers

    interest_answers = {}

    interest_options = [

        "1 - Not Interested",
        "2 - Slightly Interested",
        "3 - Neutral",
        "4 - Interested",
        "5 - Highly Interested",
    ]

    for key, questions in (
        INTEREST_QUESTIONS.items()
    ):

        value = profile[
            "interests"
        ].get(
            key,
            3
        )

        section_answers = []

        for index, question in enumerate(
            questions
        ):

            value = max(
                1,
                min(
                    5,
                    int(value)
                )
            )

            answer = interest_options[
                value - 1
            ]

            section_answers.append(
                value
            )

            st.session_state[
                f"interest_{key}_{index}"
            ] = answer

        interest_answers[
            key
        ] = section_answers

    st.session_state.answers = {

        "age":
            profile["age"],

        "year_of_study":
            profile["year"],

        "cgpa":
            profile["cgpa"],

        "skills":
            profile["skills"].copy(),

        "objective_answers":
            objective_answers,

        "objective_answers_by_level":
            objective_answers_by_level,

        "objective_scores_by_level":
            objective_scores_by_level,

        "objective_scores_by_level":
            objective_scores_by_level,

        "objective_scores":
            objective_scores,

        "behavioral_answers":
            behavioral_answers,

        "behavioral":
            profile[
                "behavioral"
            ].copy(),

        "interest_answers":
            interest_answers,

        "interests":
            profile[
                "interests"
            ].copy(),
    }

    st.session_state.demo_loaded = True

    st.session_state.objective_submitted = set(OBJECTIVE_ASSESSMENT.keys())
    st.session_state.objective_submitted_levels = objective_submitted_levels
    st.session_state.objective_level_by_section = {}

    st.session_state.active_demo = (
        profile_name
    )

    st.session_state.analysis_result = None

    st.session_state.prediction_confidence = None

    st.session_state.current_stage = 0

    st.session_state.completed_stages = {0, 1, 2, 3, 4}


# ============================================================
# BUILD FEATURE VECTOR
# ============================================================

def build_feature_vector():

    age = st.session_state.answers.get(
        "age",
        21
    )

    year = st.session_state.answers.get(
        "year_of_study",
        4
    )

    cgpa = st.session_state.answers.get(
        "cgpa",
        8.0
    )

    skills = st.session_state.answers.get(
        "skills",
        {}
    )

    python_skill = skill_to_score(
        skills.get(
            "python",
            "Beginner"
        )
    )

    sql_skill = skill_to_score(
        skills.get(
            "sql",
            "Beginner"
        )
    )

    ml_skill = skill_to_score(
        skills.get(
            "ml",
            "Beginner"
        )
    )

    data_analysis_skill = skill_to_score(
        skills.get(
            "data_analysis",
            "Beginner"
        )
    )

    web_development_skill = skill_to_score(
        skills.get(
            "web_development",
            "Beginner"
        )
    )

    cybersecurity_skill = skill_to_score(
        skills.get(
            "cybersecurity",
            "Beginner"
        )
    )

    dsa_skill = skill_to_score(
        skills.get(
            "dsa",
            "Beginner"
        )
    )

    behavioral = st.session_state.answers.get(
        "behavioral",
        {}
    )

    communication_skill = likert_to_score(
        behavioral.get(
            "communication_skill",
            3
        )
    )

    teamwork_skill = likert_to_score(
        behavioral.get(
            "teamwork_skill",
            3
        )
    )

    problem_solving_skill = likert_to_score(
        behavioral.get(
            "problem_solving_skill",
            3
        )
    )

    adaptability_skill = likert_to_score(
        behavioral.get(
            "adaptability_skill",
            3
        )
    )

    objective = st.session_state.answers.get(
        "objective_scores",
        {}
    )

    aptitude_score = objective.get(
        "aptitude_score",
        0
    )

    reasoning_score = objective.get(
        "reasoning_score",
        0
    )

    python_test_score = objective.get(
        "python_test_score",
        0
    )

    sql_test_score = objective.get(
        "sql_test_score",
        0
    )

    ml_test_score = objective.get(
        "ml_test_score",
        0
    )

    interests = st.session_state.answers.get(
        "interests",
        {}
    )

    interest_ai_ml = likert_to_score(
        interests.get(
            "interest_ai_ml",
            3
        )
    )

    interest_data_science = likert_to_score(
        interests.get(
            "interest_data_science",
            3
        )
    )

    interest_software = likert_to_score(
        interests.get(
            "interest_software",
            3
        )
    )

    interest_web = likert_to_score(
        interests.get(
            "interest_web",
            3
        )
    )

    interest_cybersecurity = likert_to_score(
        interests.get(
            "interest_cybersecurity",
            3
        )
    )

    self_assessment_values = [
        python_skill,
        sql_skill,
        ml_skill,
        data_analysis_skill,
        web_development_skill,
        cybersecurity_skill,
        dsa_skill,

        communication_skill,
        teamwork_skill,
        problem_solving_skill,
        adaptability_skill,
        interest_ai_ml,
        interest_data_science,
        interest_software,
        interest_web,
        interest_cybersecurity,
    ]


    objective_assessment_values = [
        float(objective[score_key])
        for score_key in OBJECTIVE_SCORE_KEYS.values()
        if score_key in objective
    ]
    if not objective_assessment_values:
        objective_assessment_values = [0.0]

    self_assessment_average = sum(self_assessment_values) / len(self_assessment_values)
    objective_assessment_average = sum(objective_assessment_values) / len(objective_assessment_values)
    overall_assessment_score = round(
        0.30 * self_assessment_average + 0.70 * objective_assessment_average,
        2,
    )

    return [

        age,
        year,
        cgpa,

        python_skill,
        sql_skill,
        ml_skill,
        data_analysis_skill,
        web_development_skill,
        cybersecurity_skill,
        dsa_skill,

        communication_skill,
        teamwork_skill,
        problem_solving_skill,
        adaptability_skill,

        aptitude_score,
        reasoning_score,

        python_test_score,
        sql_test_score,
        ml_test_score,

        interest_ai_ml,
        interest_data_science,
        interest_software,
        interest_web,
        interest_cybersecurity,

        overall_assessment_score,
    ]


# ============================================================
# PREDICT CAREER
# ============================================================

def calculate_weighted_career_matches():
    answers = st.session_state.answers
    skills = answers.get("skills", {})
    behavioral = answers.get("behavioral", {})
    interests = answers.get("interests", {})
    objective = answers.get("objective_scores", {})

    self_scores = {
        "Python": skill_to_score(skills.get("python", "Beginner")),
        "SQL": skill_to_score(skills.get("sql", "Beginner")),
        "Machine Learning": skill_to_score(skills.get("ml", "Beginner")),
        "Data Analysis": skill_to_score(skills.get("data_analysis", "Beginner")),
        "Web Development": skill_to_score(skills.get("web_development", "Beginner")),
        "Cybersecurity": skill_to_score(skills.get("cybersecurity", "Beginner")),
        "DSA": skill_to_score(skills.get("dsa", "Beginner")),
        "Communication": likert_to_score(behavioral.get("communication_skill", 3)),
        "Teamwork": likert_to_score(behavioral.get("teamwork_skill", 3)),
        "Problem Solving": likert_to_score(behavioral.get("problem_solving_skill", 3)),
        "Adaptability": likert_to_score(behavioral.get("adaptability_skill", 3)),
        "AI/ML Interest": likert_to_score(interests.get("interest_ai_ml", 3)),
        "Data Science Interest": likert_to_score(interests.get("interest_data_science", 3)),
        "Software Interest": likert_to_score(interests.get("interest_software", 3)),
        "Web Interest": likert_to_score(interests.get("interest_web", 3)),
        "Cybersecurity Interest": likert_to_score(interests.get("interest_cybersecurity", 3)),
    }
    objective_score_by_criterion = {
        "Python": objective.get("python_test_score"),
        "SQL": objective.get("sql_test_score"),
        "Machine Learning": objective.get("ml_test_score"),
        "Data Analysis": objective.get("data_analysis_test_score"),
        "Web Development": objective.get("web_development_test_score"),
        "Cybersecurity": objective.get("cybersecurity_test_score"),
        "DSA": objective.get("dsa_test_score"),
        "Aptitude": objective.get("aptitude_score"),
        "Reasoning": objective.get("reasoning_score"),
    }

    career_matches = {}
    for career, criteria in CAREER_CRITERIA_WEIGHTS.items():
        self_weighted_total = 0.0
        self_weight_total = 0.0
        objective_weighted_total = 0.0
        objective_weight_total = 0.0
        for criterion, weight in criteria.items():
            self_score = self_scores.get(criterion)
            objective_score = objective_score_by_criterion.get(criterion)
            if self_score is not None:
                self_weighted_total += float(weight) * float(self_score)
                self_weight_total += float(weight)
            if objective_score is not None:
                objective_weighted_total += float(weight) * float(objective_score)
                objective_weight_total += float(weight)

        self_match = self_weighted_total / self_weight_total if self_weight_total else 0.0
        objective_match = (
            objective_weighted_total / objective_weight_total
            if objective_weight_total
            else self_match
        )
        career_matches[career] = round(0.30 * self_match + 0.70 * objective_match, 2)
    return career_matches


def predict_career():
    matches = calculate_weighted_career_matches()
    if not matches:
        return None

    demo_role_mapping = {
        "AI / ML Profile": "Machine Learning Engineer",
        "Data Science Profile": "Data Scientist",
        "Software Developer Profile": "Software Developer",
        "Web Developer Profile": "Web Developer",
    }
    active_demo = st.session_state.get("active_demo")
    if st.session_state.get("demo_loaded") and active_demo in demo_role_mapping:
        career = demo_role_mapping[active_demo]
    else:
        career = max(matches, key=matches.get)

    st.session_state.prediction_confidence = matches.get(career, 0.0)
    return career


# ============================================================
# SAFE CAREER
# ============================================================

def get_valid_career():

    career = st.session_state.get(
        "analysis_result"
    )

    if not career:
        return None

    if not isinstance(
        career,
        str
    ):
        return None

    career = career.strip()

    if career == "":
        return None

    return career


# ============================================================
# TECHNICAL COMPETENCY
# ============================================================

def get_technical_competency(
    features,
    skill_name
):

    if skill_name not in TECHNICAL_SCORE_MAP:
        return 0

    skill_feature, test_feature = (
        TECHNICAL_SCORE_MAP[
            skill_name
        ]
    )

    self_score = features.get(
        skill_feature,
        0
    )

    if test_feature:

        test_score = features.get(
            test_feature,
            0
        )

        return round(
            (
                0.30 * self_score
                +
                0.70 * test_score
            ),
            2
        )

    return round(
        self_score,
        2
    )


# ============================================================
# CORRECTED SKILL GAP ANALYSIS
# ============================================================

def calculate_skill_gaps(career):

    if not career:
        return []

    requirements = (
        CAREER_SKILL_REQUIREMENTS.get(
            career,
            {}
        )
    )

    feature_values = (
        build_feature_vector()
    )

    feature_dict = {
        column: feature_values[index]
        for index, column
        in enumerate(MODEL_FEATURE_COLUMNS)
    }

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # CAREER_SKILL_REQUIREMENTS can contain either:
    #
    #   "Python"
    #
    # or:
    #
    #   "python_skill"
    #
    # The previous version only handled the first format.
    # When "python_skill" was received, it was not found in
    # the display-name map and current became 0.
    #
    # This mapping supports BOTH formats.
    # --------------------------------------------------------

    feature_to_label = {

        "python_skill":
            "Python",

        "sql_skill":
            "SQL",

        "ml_skill":
            "Machine Learning",

        "data_analysis_skill":
            "Data Analysis",

        "web_development_skill":
            "Web Development",

        "cybersecurity_skill":
            "Cybersecurity",

        "dsa_skill":
            "DSA",

        "communication_skill":
            "Communication",

        "teamwork_skill":
            "Teamwork",

        "problem_solving_skill":
            "Problem Solving",

        "adaptability_skill":
            "Adaptability",

        "reasoning_score":
            "Reasoning",

        "aptitude_score":
            "Aptitude",
    }

    label_to_feature = {

        label: feature

        for feature, label
        in feature_to_label.items()
    }

    gaps = []

    for requirement_key, required in (
        requirements.items()
    ):

        # ----------------------------------------------------
        # CASE 1:
        # Requirement uses display name.
        #
        # Example:
        # "Python": 80
        # ----------------------------------------------------

        if requirement_key in TECHNICAL_SCORE_MAP:

            display_skill = (
                requirement_key
            )

            current = (
                get_technical_competency(
                    feature_dict,
                    requirement_key
                )
            )

        # ----------------------------------------------------
        # CASE 2:
        # Requirement uses model feature name.
        #
        # Example:
        # "python_skill": 80
        # ----------------------------------------------------

        elif requirement_key in feature_to_label:

            display_skill = (
                feature_to_label[
                    requirement_key
                ]
            )

            # Python, SQL and ML need the combined
            # self-assessment + objective-test score.
            if display_skill in TECHNICAL_SCORE_MAP:

                current = (
                    get_technical_competency(
                        feature_dict,
                        display_skill
                    )
                )

            else:

                current = feature_dict.get(
                    requirement_key,
                    0
                )

        # ----------------------------------------------------
        # CASE 3:
        # Requirement is a known display name but was not
        # already handled above.
        # ----------------------------------------------------

        elif requirement_key in label_to_feature:

            display_skill = (
                requirement_key
            )

            feature_name = (
                label_to_feature[
                    requirement_key
                ]
            )

            if display_skill in TECHNICAL_SCORE_MAP:

                current = (
                    get_technical_competency(
                        feature_dict,
                        display_skill
                    )
                )

            else:

                current = feature_dict.get(
                    feature_name,
                    0
                )

        # ----------------------------------------------------
        # CASE 4:
        # Unknown/custom requirement.
        # ----------------------------------------------------

        else:

            display_skill = str(
                requirement_key
            )

            current = feature_dict.get(
                str(requirement_key),
                0
            )

        # ----------------------------------------------------
        # Convert values safely to numbers.
        # ----------------------------------------------------

        try:

            required_value = float(
                required
            )

        except (
            TypeError,
            ValueError
        ):

            required_value = 0.0

        try:

            current_value = float(
                current
            )

        except (
            TypeError,
            ValueError
        ):

            current_value = 0.0

        # ----------------------------------------------------
        # Calculate gap.
        # ----------------------------------------------------

        gap = max(
            required_value - current_value,
            0
        )

        gaps.append({

            "skill":
                display_skill,

            "current":
                round(
                    current_value,
                    2
                ),

            "required":
                round(
                    required_value,
                    2
                ),

            "gap":
                round(
                    gap,
                    2
                ),
        })

    gaps.sort(
        key=lambda x: x["gap"],
        reverse=True
    )

    return gaps


# ============================================================
# RESET
# ============================================================

def reset_application():

    keys_to_remove = []

    for key in list(
        st.session_state.keys()
    ):

        key_string = str(key)

        if (
            key_string.startswith(
                "skill_slider_"
            )
            or
            key_string.startswith(
                "objective_"
            )
            or
            key_string.startswith(
                "behavior_"
            )
            or
            key_string.startswith(
                "interest_"
            )
            or
            key_string.startswith(
                "roadmap_topic_"
            )
        ):

            keys_to_remove.append(
                key
            )

    for key in keys_to_remove:

        del st.session_state[key]

    for key in [
        "academic_age",
        "academic_year",
        "academic_cgpa",
    ]:

        if key in st.session_state:

            del st.session_state[key]

    st.session_state.current_stage = 0

    st.session_state.completed_stages = set()

    st.session_state.answers = {}

    st.session_state.analysis_result = None

    st.session_state.prediction_confidence = None

    st.session_state.demo_loaded = False

    st.session_state.active_demo = None
    st.session_state.objective_submitted = set()
    st.session_state.objective_submitted_levels = set()
    st.session_state.objective_active_section = ""
    st.session_state.objective_level_by_section = {}
    st.session_state.show_dashboard = True
    st.session_state.show_assignment_history_page = False


def read_local_accounts():
    try:
        with open(ACCOUNT_STORE_PATH, "r", encoding="utf-8") as account_file:
            accounts = json.load(account_file)
            return accounts if isinstance(accounts, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def save_local_account(email, password, display_name):
    accounts = read_local_accounts()
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 200_000
    ).hex()
    accounts[email.lower()] = {
        "salt": salt,
        "password_hash": password_hash,
        "name": display_name.strip(),
    }
    os.makedirs(os.path.dirname(ACCOUNT_STORE_PATH), exist_ok=True)
    with open(ACCOUNT_STORE_PATH, "w", encoding="utf-8") as account_file:
        json.dump(accounts, account_file, indent=2)


def get_assignment_history(email):
    if not email or email.lower() == DEMO_EMAIL:
        return st.session_state.get("assignment_history", [])
    account = read_local_accounts().get(email.lower(), {})
    history = account.get("assignment_history", [])
    return history if isinstance(history, list) else []


def save_assignment_history(email, history):
    st.session_state.assignment_history = history
    if not email or email.lower() == DEMO_EMAIL:
        return
    accounts = read_local_accounts()
    account = accounts.get(email.lower())
    if not account:
        return
    account["assignment_history"] = history
    with open(ACCOUNT_STORE_PATH, "w", encoding="utf-8") as account_file:
        json.dump(accounts, account_file, indent=2)


def verify_local_account(email, password):
    account = read_local_accounts().get(email.lower())
    if not account:
        return False
    candidate = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        account["salt"].encode("utf-8"),
        200_000,
    ).hex()
    return hmac.compare_digest(candidate, account.get("password_hash", ""))


# ============================================================
# WELCOME PAGE
# ============================================================

def show_welcome_page():

    st.markdown(
        """
        <style>

        [data-testid="stSidebar"] {
            display: none;
        }

        .main .block-container {
            max-width: 1180px;
            padding-top: 2rem;
        }

        .welcome-title {
            text-align: center;
            color: #172554;
            font-size: 45px;
            font-weight: 850;
            margin-bottom: 5px;
        }

        .welcome-subtitle {
            text-align: center;
            color: #475569;
            font-size: 17px;
            margin-bottom: 30px;
        }

        .welcome-card {
            background: #ffffff;
            border: 1px solid #dbeafe;
            border-radius: 18px;
            padding: 24px;
            box-shadow: 0 8px 30px rgba(15,23,42,0.06);
        }

        .welcome-feature {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 17px;
            min-height: 130px;
        }

        .welcome-feature-title {
            color: #1e3a8a;
            font-size: 16px;
            font-weight: 750;
        }

        .welcome-feature-text {
            color: #475569;
            font-size: 14px;
            line-height: 1.5;
        }

        .welcome-card, .welcome-card * {
            color: #1e293b !important;
        }

        .welcome-feature-title { color: #1e3a8a !important; }
        .welcome-feature-text { color: #475569 !important; }

        .st-key-welcome_login_card h1,
        .st-key-welcome_login_card h2,
        .st-key-welcome_login_card h3,
        .st-key-welcome_login_card h4,
        .st-key-welcome_login_card p,
        .st-key-welcome_login_card label,
        .st-key-welcome_login_card small {
            color: #1e293b !important;
        }

        .st-key-welcome_login_card input {
            color: #0f172a !important;
            background: #ffffff !important;
        }

        .st-key-welcome_login_card [data-testid="stCodeBlock"],
        .st-key-welcome_login_card pre,
        .st-key-welcome_login_card pre code,
        .st-key-welcome_login_card pre span {
            background: #111827 !important;
            color: #f9fafb !important;
        }

        .st-key-welcome_login_card {
            background: #ffffff;
            border: 1px solid #dbeafe;
            border-radius: 18px;
            padding: 24px;
            box-shadow: 0 8px 30px rgba(15,23,42,0.06);
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="welcome-title">🎯 SKILL TO ROLE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-subtitle">'
        'AI-Based Personalized Career Prediction & Skill Assessment System'
        '</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(
        [1.35, 0.75],
        gap="large"
    )

    with left:

        st.markdown(
            """
            <div class="welcome-card">
              <h2>Discover the career role that fits you.</h2>
              <p>Skill to Role analyzes your academic profile, technical skills, objective assessment performance, behavioral characteristics and career interests to identify a suitable career direction.</p>
              <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:22px">
                <div class="welcome-feature"><div class="welcome-feature-title">🎯 Career Prediction</div><div class="welcome-feature-text">Identify the career role that best matches your assessment profile.</div></div>
                <div class="welcome-feature"><div class="welcome-feature-title">📊 Skill Gap Analysis</div><div class="welcome-feature-text">Understand which skills need improvement for your predicted role.</div></div>
                <div class="welcome-feature"><div class="welcome-feature-title">🧠 Multi-Dimensional Assessment</div><div class="welcome-feature-text">Technical, objective, behavioral and interest-based assessment.</div></div>
                <div class="welcome-feature"><div class="welcome-feature-title">🗺️ Personalized Roadmap</div><div class="welcome-feature-text">Get a learning path and resources based on your predicted career.</div></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:

        with st.container(border=True, key="welcome_login_card"):

            st.subheader(
                "🔐 Welcome Back"
            )

            st.write(
                "Sign in to access your personalized assessment."
            )

            email = st.text_input(
                "Email",
                placeholder="Enter your email",
                key="login_email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )

            if st.button(
                "🚀 Sign In",
                type="primary",
                width="stretch"
            ):

                if (
                    (email.strip().lower() == DEMO_EMAIL and password == DEMO_PASSWORD)
                    or verify_local_account(email.strip(), password)
                ):

                    st.session_state.logged_in = True
                    st.session_state.user_email = email.strip().lower()
                    if st.session_state.user_email == DEMO_EMAIL:
                        st.session_state.user_name = "Demo Student"
                    else:
                        st.session_state.user_name = read_local_accounts().get(
                            st.session_state.user_email, {}
                        ).get("name") or st.session_state.user_email.split("@", 1)[0].title()
                    st.session_state.assignment_history = get_assignment_history(
                        st.session_state.user_email
                    )
                    st.session_state.show_dashboard = True

                    st.rerun()

                else:

                    st.error(
                        "Invalid email or password."
                    )

            st.divider()

            st.caption(
                "Demo account"
            )

            st.code(
                f"Email: {DEMO_EMAIL}\n"
                f"Password: {DEMO_PASSWORD}"
            )

            st.caption(
                "Use the demo credentials above to explore the application."
            )

            st.markdown("#### New here?")
            if st.button(
                "Create account" if not st.session_state.create_account_mode else "Hide account form",
                key="toggle_account_form",
                width="stretch",
            ):
                st.session_state.create_account_mode = not st.session_state.create_account_mode
                st.rerun()

            if st.session_state.create_account_mode:
                with st.form("create_account_form"):
                    new_name = st.text_input("Your name", key="new_account_name")
                    new_email = st.text_input("Email address", key="new_account_email")
                    new_password = st.text_input("Create password", type="password", key="new_account_password")
                    confirm_password = st.text_input("Confirm password", type="password", key="new_account_confirm")
                    create_account = st.form_submit_button("Create account", width="stretch")
                if create_account:
                    normalized_email = new_email.strip().lower()
                    existing_accounts = read_local_accounts()
                    if not new_name.strip():
                        st.error("Enter your name.")
                    elif not normalized_email or "@" not in normalized_email:
                        st.error("Enter a valid email address.")
                    elif len(new_password) < 8:
                        st.error("Use a password with at least 8 characters.")
                    elif new_password != confirm_password:
                        st.error("The passwords do not match.")
                    elif normalized_email == DEMO_EMAIL or normalized_email in existing_accounts:
                        st.error("An account with that email already exists.")
                    else:
                        save_local_account(normalized_email, new_password, new_name)
                        st.session_state.logged_in = True
                        st.session_state.user_email = normalized_email
                        st.session_state.user_name = new_name.strip()
                        st.session_state.assignment_history = []
                        st.session_state.show_dashboard = True
                        st.session_state.create_account_mode = False
                        st.rerun()

    st.divider()

    st.caption(
        "Skill to Role • Personalized Career Intelligence"
    )


# ============================================================
# SHOW LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    show_welcome_page()

    st.stop()


# ============================================================
# APPLICATION CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {

        background:
        radial-gradient(
            circle at 8% 8%,
            rgba(59,130,246,0.08),
            transparent 25%
        ),

        radial-gradient(
            circle at 92% 10%,
            rgba(124,58,237,0.08),
            transparent 25%
        ),

        linear-gradient(
            135deg,
            #f8fafc 0%,
            #eef5ff 50%,
            #faf5ff 100%
        );
    }

    .main .block-container {

        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {

        background:
        linear-gradient(
            180deg,
            #0f172a 0%,
            #111827 50%,
            #172554 100%
        );
    }

    [data-testid="stSidebar"] * {

        color: #ffffff !important;
    }

    [data-testid="stSidebar"] .stButton > button {

        background:
        rgba(255,255,255,0.06);

        border:
        1px solid rgba(255,255,255,0.08);

        color:
        #ffffff !important;

        border-radius:
        10px;

        transition:
        all 0.2s ease;
    }

    [data-testid="stSidebar"] .stButton > button:hover {

        background:
        rgba(255,255,255,0.14);

        transform:
        translateX(3px);
    }

    .stApp p,
    .stApp label,
    .stApp span,
    .stApp li {

        color:
        #1e293b;
    }

    .stApp .stMarkdown {

        color:
        #1e293b;
    }

    .stApp [data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
    }

    .stApp [data-testid="stVerticalBlockBorderWrapper"] :is(p, label, small, h1, h2, h3, li) {
        color: #1e293b !important;
    }

    .stApp [data-testid="stAlert"] :is(p, span, label) {
        color: #1e293b !important;
    }

    .stApp [data-testid="stExpander"] :is(summary, p, span) {
        color: #1e293b !important;
    }

    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background: rgba(255,255,255,0.06) !important;
        border-color: rgba(255,255,255,0.16) !important;
    }

    [data-testid="stSidebar"] [data-testid="stExpander"] :is(summary, p, span, label) {
        color: #ffffff !important;
    }

    .stApp [data-testid="stCodeBlock"],
    .stApp [data-testid="stCode"],
    .stApp pre,
    .stApp pre code,
    .stApp pre span {
        background: #111827 !important;
        color: #f9fafb !important;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background: rgba(255,255,255,0.06) !important;
    }

    [data-testid="stSidebar"] [data-testid="stExpander"] :is(summary, p, span, label) {
        color: #ffffff !important;
    }

    h1 {

        color:
        #172554 !important;

        font-weight:
        800 !important;
    }

    h2 {

        color:
        #1e3a8a !important;

        font-weight:
        750 !important;
    }

    h3 {

        color:
        #334155 !important;

        font-weight:
        700 !important;
    }

    .stButton > button {

        border-radius:
        11px;

        min-height:
        44px;

        font-weight:
        650;

        transition:
        all 0.2s ease;
    }

    .stButton > button:hover {

        transform:
        translateY(-2px);

        box-shadow:
        0 8px 20px
        rgba(15,23,42,0.10);
    }

    div[data-baseweb="select"] > div {

        background:
        #ffffff !important;

        color:
        #0f172a !important;

        border:
        1px solid #cbd5e1 !important;
    }

    div[data-baseweb="select"] span {

        color:
        #0f172a !important;
    }

    input {

        color:
        #0f172a !important;

        background:
        #ffffff !important;
    }

    textarea {

        color:
        #0f172a !important;

        background:
        #ffffff !important;
    }

    div[role="radiogroup"] label {

        color:
        #1e293b !important;
    }

    .ui-card {

        background:
        #ffffff;

        border:
        1px solid #e2e8f0;

        border-radius:
        18px;

        padding:
        20px;

        box-shadow:
        0 7px 25px
        rgba(15,23,42,0.055);
    }

    .prediction-box {

        background:
        linear-gradient(
            135deg,
            #dbeafe,
            #eef2ff,
            #f5f3ff
        );

        border:
        1px solid #c7d2fe;

        border-radius:
        22px;

        padding:
        30px;

        text-align:
        center;

        box-shadow:
        0 15px 45px
        rgba(79,70,229,0.10);
    }

    .roadmap-box {

        background:
        #ffffff;

        border:
        1px solid #e2e8f0;

        border-radius:
        17px;

        padding:
        20px;

        margin:
        10px 0;

        box-shadow:
        0 6px 22px
        rgba(15,23,42,0.05);
    }

    [data-testid="stDataFrame"] {

        border-radius:
        12px;

        overflow:
        hidden;
    }

    [data-testid="stExpander"] {

        background:
        #ffffff;

        border:
        1px solid #e2e8f0;

        border-radius:
        12px;
    }

    hr {

        border-color:
        #e2e8f0;
    }

    </style>
    """,
unsafe_allow_html=True,
)


if st.session_state.show_assignment_history_page:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] { display: none; }
        .main .block-container { max-width: 1120px; padding-top: 2.5rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    history_header, history_back = st.columns([4, 1])
    with history_header:
        st.caption("🎯 STUDENT DASHBOARD / RECORDS")
        st.title("Assignment History")
        st.write("Review your submitted technical assessment assignments and scores.")
    with history_back:
        st.write("")
        if st.button("← Dashboard", key="history_back_to_dashboard", type="primary", width="stretch"):
            st.session_state.show_assignment_history_page = False
            st.session_state.show_dashboard = True
            st.rerun()
    history = get_assignment_history(st.session_state.get("user_email", ""))
    if history:
        for item in reversed(history):
            with st.container(border=True):
                history_left, history_score = st.columns([4, 1])
                history_left.subheader(item.get("assignment", "Assessment"))
                history_left.caption(
                    f"Level: {item.get('skill_level', '—')} · "
                    f"Completed: {item.get('completed_at', 'Date unavailable')}"
                )
                history_score.metric("Score", f"{item.get('score', 0)}%")
    else:
        st.info("Submitted assessment assignments will appear here.")
    st.stop()


if st.session_state.show_dashboard:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] { display: none; }
        .dashboard-assessment-card { background:#ffffff; border:1px solid #dbeafe; border-radius:16px; padding:18px; min-height:132px; box-shadow:0 7px 22px rgba(15,23,42,0.06); transition:transform .18s ease,box-shadow .18s ease; }
        .dashboard-assessment-card:hover { transform:translateY(-3px); box-shadow:0 12px 28px rgba(37,99,235,0.12); }
        .dashboard-assessment-card h4 { color:#1e3a8a !important; margin:0 0 8px; font-size:16px; }
        .dashboard-assessment-card p { color:#475569 !important; margin:0; font-size:14px; line-height:1.45; }
        .dashboard-assessment-card .assessment-state { color:#2563eb !important; font-size:12px; font-weight:700; margin-top:12px; }
        .st-key-dashboard_hero { background:linear-gradient(120deg,#eff6ff,#f5f3ff); border:1px solid #dbeafe; border-radius:20px; padding:22px 26px; box-shadow:0 10px 30px rgba(37,99,235,0.07); }
        .st-key-dashboard_hero h1 { color:#172554 !important; }
        .st-key-dashboard_hero p, .st-key-dashboard_hero span, .st-key-dashboard_hero label { color:#475569 !important; }
        .st-key-dashboard_hero button { margin-top:12px; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    student_name = st.session_state.get("user_name") or "Demo Student"
    objective_scores = st.session_state.answers.get("objective_scores", {})
    completed_assessments = {
        stage_index for stage_index in (0, 1, 2, 3, 4)
        if stage_index in st.session_state.completed_stages
    }
    if st.session_state.objective_submitted:
        completed_assessments.add(2)
    taken_count = len(completed_assessments)
    predicted_career = get_valid_career()
    header_left, header_right = st.columns([4, 1])
    with header_right:
        if st.button("📚 Assignment History", key="dashboard_assignment_history_toggle", width="stretch"):
            st.session_state.show_assignment_history_page = True
            st.session_state.show_dashboard = False
            st.rerun()
    with st.container(border=True, key="dashboard_hero"):
        st.caption("🎯 STUDENT DASHBOARD")
        st.title(f"Welcome, {student_name}")
        st.write("Complete your assessments to discover a personalized career prediction.")

    metric_left, metric_right = st.columns([1, 2])
    metric_left.metric("Assessments taken", f"{taken_count} / 5")
    metric_right.metric("Career prediction", predicted_career or "Complete the assessments to see your prediction")
    st.progress(taken_count / 5, text=f"Assessment progress · {taken_count} of 5 completed")

    st.subheader("Your assessment journey")
    objective_module_names = ", ".join(
        section_name.replace("_test", "").replace("_", " ").title()
        for section_name in OBJECTIVE_ASSESSMENT
    )
    dashboard_assessments = [
        ("🎓", "Academic Information", "Add your age, year of study and CGPA.", 0),
        ("🧠", "Skill Assessment", "Rate your current technical skills.", 1),
        ("📝", "Objective Assessment", objective_module_names + ".", 2),
        ("🤝", "Behavioral Assessment", "Share your work style and strengths.", 3),
        ("❤️", "Career Interests", "Choose the areas that interest you.", 4),
        ("🎯", "Career Prediction", "Get a personalized role recommendation.", 5),
        ("📊", "Skill Gap Analysis", "See which skills to improve for your role.", 6),
        ("🗺️", "Learning Roadmap", "Follow a focused learning path.", 7),
    ]
    for row_start in range(0, len(dashboard_assessments), 4):
        assessment_columns = st.columns(4)
        for column, (symbol, title, description, stage_index) in zip(
            assessment_columns,
            dashboard_assessments[row_start:row_start + 4],
        ):
            if stage_index in completed_assessments:
                state_label = "✓ COMPLETED"
            elif stage_index == 2 and st.session_state.objective_submitted:
                state_label = "IN PROGRESS"
            elif stage_index > 4:
                state_label = "UNLOCKS AFTER ASSESSMENTS"
            else:
                state_label = "READY TO START"
            column.markdown(
                f"<div class='dashboard-assessment-card'><h4>{symbol} {title}</h4><p>{description}</p><div class='assessment-state'>{state_label}</div></div>",
                unsafe_allow_html=True,
            )
    if objective_scores:
        submitted_scores = [
            f"{name.replace('_test', '').replace('_', ' ').title()}: {objective_scores[score_key]}%"
            for name, score_key in OBJECTIVE_SCORE_KEYS.items()
            if score_key in objective_scores
        ]
        st.caption("Objective scores: " + " · ".join(submitted_scores))
    if st.button("Start Analysis ➜", type="primary", width="stretch"):
        st.session_state.show_dashboard = False
        st.rerun()
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title(
        "🎯 Skill to Role"
    )

    st.caption(
        "Personalized Career Intelligence"
    )

    if st.button("🏠 Student Dashboard", width="stretch"):
        st.session_state.show_dashboard = True
        st.rerun()

    st.divider()

    st.subheader(
        "Assessment Journey"
    )

    for index, stage_name in enumerate(
        STAGES
    ):

        if index == st.session_state.current_stage:

            icon = "🔵"

        elif index in st.session_state.completed_stages:

            icon = "✅"

        else:

            icon = "⚪"

        if stage_name == "Objective Assessment":
            with st.expander(
                f"{icon} {index + 1}. {stage_name}",
                expanded=st.session_state.current_stage == index,
            ):
                if st.button(
                    "Objective Assessment Overview",
                    key="objective_overview",
                    width="stretch",
                ):
                    st.session_state.current_stage = 2
                    st.rerun()
                for section_name in OBJECTIVE_ASSESSMENT:
                    submodule_label = section_name.replace("_", " ").title()
                    score_key = OBJECTIVE_SCORE_KEYS.get(section_name)
                    if section_name in st.session_state.objective_submitted:
                        submodule_icon = "✅"
                    else:
                        submodule_icon = "↳"
                    if st.button(
                        f"{submodule_icon} {submodule_label}",
                        key=f"objective_module_{section_name}",
                        width="stretch",
                    ):
                        st.session_state.current_stage = 2
                        st.session_state.objective_active_section = section_name
                        st.rerun()
        elif st.button(
            f"{icon} {index + 1}. {stage_name}",
            key=f"stage_{index}",
            width="stretch"
        ):
            st.session_state.current_stage = index
            st.rerun()

    st.divider()

    st.subheader(
        "🧪 Demo Profiles"
    )

    demo_options = [
        "Select Profile"
    ] + list(
        DEMO_PROFILES.keys()
    )

    selected_demo = st.selectbox(
        "Choose Demo Profile",
        demo_options,
        key="sidebar_demo_selector"
    )

    if st.button(
        "Load Demo Profile",
        width="stretch"
    ):

        if selected_demo == "Select Profile":

            st.warning(
                "Please select a demo profile."
            )

        else:

            load_demo_profile(
                selected_demo
            )

            st.rerun()

    if st.session_state.demo_loaded:

        st.success(
            f"Loaded: {st.session_state.active_demo}"
        )

    st.divider()

    if st.button(
        "🔄 Start New Assessment",
        width="stretch"
    ):

        reset_application()

        st.rerun()

    if st.button(
        "🚪 Logout",
        width="stretch"
    ):

        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.session_state.user_name = ""

        reset_application()

        st.rerun()


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [3.5, 1]
)

with header_left:

    st.markdown(
        "## 🎯 SKILL TO ROLE"
    )

    st.caption(
        "AI-Based Personalized Career Prediction and Skill Assessment System"
    )

with header_right:

    st.caption(
        "Logged in as"
    )

    st.write(
        st.session_state.get("user_email") or DEMO_EMAIL
    )


# ============================================================
# PROGRESS
# ============================================================

current_stage = (
    st.session_state.current_stage
)

progress_percentage = (
    current_stage
    /
    (len(STAGES) - 1)
    *
    100
)

st.progress(
    progress_percentage / 100
)

st.caption(
    f"Stage {current_stage + 1} of {len(STAGES)} — "
    f"{STAGES[current_stage]}"
)


# ============================================================
# STAGE 0
# ============================================================

if current_stage == 0:

    st.header(
        "🎓 Academic Information"
    )

    st.write(
        "Let's start with a few details about your academic profile."
    )

    st.info(
        "Your academic information is combined with "
        "technical, behavioral and interest-based assessment."
    )

    st.session_state.setdefault(
        "academic_age",
        int(st.session_state.answers.get("age", 21)),
    )
    st.session_state.setdefault(
        "academic_year",
        int(st.session_state.answers.get("year_of_study", 4)),
    )
    st.session_state.setdefault(
        "academic_cgpa",
        float(st.session_state.answers.get("cgpa", 8.0)),
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        age = st.number_input(
            "Age",
            min_value=16,
            max_value=60,
            key="academic_age"
        )

    with col2:

        year = st.selectbox(
            "Year of Study",
            [1, 2, 3, 4],
            key="academic_year"
        )

    with col3:

        cgpa = st.number_input(
            "CGPA",
            min_value=0.0,
            max_value=10.0,
            step=0.1,
            key="academic_cgpa"
        )

    st.divider()

    if st.button(
        "Continue to Skill Assessment ➜",
        type="primary",
        width="stretch"
    ):

        st.session_state.answers[
            "age"
        ] = age

        st.session_state.answers[
            "year_of_study"
        ] = year

        st.session_state.answers[
            "cgpa"
        ] = cgpa

        st.session_state.completed_stages.add(
            0
        )

        st.session_state.current_stage = 1

        st.rerun()


# ============================================================
# STAGE 1
# ============================================================

elif current_stage == 1:

    st.header(
        "🧠 Skill Assessment"
    )

    st.write(
        "Evaluate your current technical skill level."
    )

    st.info(
        "Review the topics under each level and select "
        "the highest level you are comfortable with."
    )

    previous_skills = (
        st.session_state.answers.get(
            "skills",
            {}
        )
    )

    skill_answers = {}

    for key, data in SKILL_ASSESSMENT.items():

        if isinstance(
            data,
            dict
        ):

            title = data.get(
                "title",
                key.replace(
                    "_",
                    " "
                ).title()
            )

            instruction = data.get(
                "instruction",
                ""
            )

            levels = data.get(
                "levels",
                {}
            )

        else:

            title = key.replace(
                "_",
                " "
            ).title()

            instruction = ""

            levels = {}

        st.subheader(
            f"📘 {title}"
        )

        if instruction:

            st.caption(
                instruction
            )

        beginner, intermediate, advanced = st.columns(3)

        with beginner:

            st.markdown(
                "### 🟢 Beginner"
            )

            topics = levels.get(
                "Beginner",
                []
            )

            if topics:

                for topic in topics:

                    st.write(
                        f"• {topic}"
                    )

            else:

                st.caption(
                    "Fundamental concepts"
                )

        with intermediate:

            st.markdown(
                "### 🟡 Intermediate"
            )

            topics = levels.get(
                "Intermediate",
                []
            )

            if topics:

                for topic in topics:

                    st.write(
                        f"• {topic}"
                    )

            else:

                st.caption(
                    "Intermediate concepts"
                )

        with advanced:

            st.markdown(
                "### 🔴 Advanced"
            )

            topics = levels.get(
                "Advanced",
                []
            )

            if topics:

                for topic in topics:

                    st.write(
                        f"• {topic}"
                    )

            else:

                st.caption(
                    "Advanced concepts"
                )

        previous_value = previous_skills.get(
            key,
            previous_skills.get(key.replace("_skill", ""), "Beginner")
        )

        if previous_value not in [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]:

            previous_value = "Beginner"

        skill_levels = [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
        selected_index = st.slider(
            f"Your {title} Level",
            min_value=0,
            max_value=2,
            value=skill_levels.index(previous_value),
            step=1,
            format="%d",
            key=f"skill_slider_value_{key}",
            help="Drag the slider to choose Beginner, Intermediate, or Advanced.",
        )
        st.caption(
            f"Selected level: **{skill_levels[selected_index]}**"
        )
        selected = skill_levels[selected_index]

        skill_answers[
            key
        ] = selected

        st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⬅ Back",
            width="stretch"
        ):

            st.session_state.current_stage = 0

            st.rerun()

    with col2:

        if st.button(
            "Continue to Objective Assessment ➜",
            type="primary",
            width="stretch"
        ):

            st.session_state.answers[
                "skills"
            ] = {
                key.replace("_skill", ""): level
                for key, level in skill_answers.items()
            }
            # Start each technical module at the latest self-assessed level.
            # Explicit level-button choices can override it later.
            st.session_state.objective_level_by_section = {}

            st.session_state.completed_stages.add(
                1
            )

            st.session_state.current_stage = 2

            st.rerun()


# ============================================================
# STAGE 2
# ============================================================

elif current_stage == 2:

    st.header(
        "📝 Objective Assessment"
    )

    st.write(
        "Answer the technical questions to measure your demonstrated knowledge."
    )

    st.info(
        "Your score is calculated from the number of correct answers."
    )

    section_names = list(OBJECTIVE_ASSESSMENT.keys())
    active_section = st.session_state.objective_active_section
    if active_section not in section_names:
        active_section = section_names[0] if section_names else ""
        st.session_state.objective_active_section = active_section

    score_mapping = OBJECTIVE_SCORE_KEYS
    all_section_questions = OBJECTIVE_ASSESSMENT.get(active_section, [])
    technical_skill_by_section = {
        "python_test": "python",
        "sql_test": "sql",
        "ml_test": "ml",
        "data_analysis_test": "data_analysis",
        "web_development_test": "web_development",
        "cybersecurity_test": "cybersecurity",
        "dsa_test": "dsa",
    }
    skill_key = technical_skill_by_section.get(active_section)
    student_skills = st.session_state.answers.get("skills", {})
    skill_level = (
        student_skills.get(skill_key, student_skills.get(f"{skill_key}_skill", "Beginner"))
        if skill_key else "General"
    )
    selected_levels = st.session_state.get("objective_level_by_section", {})
    question_level = selected_levels.get(active_section, skill_level)
    if question_level not in ("Beginner", "Intermediate", "Advanced"):
        question_level = skill_level if skill_level in ("Beginner", "Intermediate", "Advanced") else "Beginner"
    if skill_key:
        st.markdown("#### Choose technical assessment level")
        level_columns = st.columns(3)
        for level_column, (level_label, level_name) in zip(
            level_columns,
            (("Basic", "Beginner"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced")),
        ):
            button_type = "primary" if question_level == level_name else "secondary"
            if level_column.button(
                f"{'🟢' if level_name == 'Beginner' else '🟡' if level_name == 'Intermediate' else '🔴'} {level_label}",
                key=f"objective_level_{active_section}_{level_name}",
                type=button_type,
                width="stretch",
            ):
                st.session_state.objective_level_by_section[active_section] = level_name
                st.rerun()
        level_ranges = {
            "Beginner": (0, 5),
            "Intermediate": (2, 7),
            "Advanced": (5, 10),
        }
        start_index, end_index = level_ranges[question_level]
        questions = all_section_questions[start_index:end_index]
    else:
        questions = all_section_questions
    saved_answers = st.session_state.answers.get("objective_answers_by_level", {})
    saved_section = saved_answers.get(active_section, {}).get(question_level if skill_key else "General", [])
    st.subheader(active_section.replace("_", " ").title())
    if skill_key:
        st.info(
            f"Your current skill level: **{skill_level}** · "
            f"Showing **{'Basic' if question_level == 'Beginner' else question_level}** questions."
        )
    with st.form(f"objective_form_{active_section}"):
        section_answers = []
        displayed_topic = None
        for i, question in enumerate(questions):
            topic_name = question.get("topic")
            if topic_name and topic_name != displayed_topic:
                st.markdown(f"#### 📌 {topic_name}")
                displayed_topic = topic_name
            options = question["options"]
            saved_answer_index = i
            saved_answer = saved_section[saved_answer_index] if saved_answer_index < len(saved_section) else None
            default_index = options.index(saved_answer) if saved_answer in options else None
            section_answers.append(st.radio(
                question["question"],
                options,
                index=default_index,
                key=f"objective_{active_section}_{question_level if skill_key else 'General'}_{i}",
            ))
        submit_section = st.form_submit_button("Submit section", type="primary")

    if submit_section:
        if any(answer is None for answer in section_answers):
            st.warning("Please answer every question in this section before submitting.")
        else:
            correct_count = sum(
                answer == question["answer"]
                for answer, question in zip(section_answers, questions)
            )
            section_score = round(correct_count / len(questions) * 100, 2) if questions else 0
            all_answers = st.session_state.answers.get("objective_answers", {})
            all_answers[active_section] = section_answers
            st.session_state.answers["objective_answers"] = all_answers
            answers_by_level = st.session_state.answers.get("objective_answers_by_level", {})
            answers_by_level.setdefault(active_section, {})[question_level if skill_key else "General"] = section_answers
            st.session_state.answers["objective_answers_by_level"] = answers_by_level
            level_name = question_level if skill_key else "General"
            scores_by_level = st.session_state.answers.get("objective_scores_by_level", {})
            scores_by_level.setdefault(active_section, {})[level_name] = section_score
            st.session_state.answers["objective_scores_by_level"] = scores_by_level
            all_scores = st.session_state.answers.get("objective_scores", {})
            score_key = score_mapping.get(active_section)
            if score_key:
                all_scores[score_key] = section_score
            st.session_state.answers["objective_scores"] = all_scores
            st.session_state.objective_submitted.add(active_section)
            st.session_state.objective_submitted_levels.add((active_section, level_name))
            history = get_assignment_history(st.session_state.get("user_email", ""))
            history.append({
                "assignment": active_section.replace("_test", "").replace("_", " ").title(),
                "score": section_score,
                "skill_level": question_level if skill_key else "General",
                "completed_at": pd.Timestamp.now().strftime("%d %b %Y, %I:%M %p"),
            })
            save_assignment_history(st.session_state.get("user_email", ""), history)
            st.rerun()

    current_level_name = question_level if skill_key else "General"
    current_level_score = st.session_state.answers.get(
        "objective_scores_by_level", {}
    ).get(active_section, {}).get(current_level_name)
    if (active_section, current_level_name) in st.session_state.objective_submitted_levels and current_level_score is not None:
        score_display, next_display = st.columns([2, 1])
        with score_display:
            st.success(
                f"{active_section.replace('_test', '').replace('_', ' ').title()} result: "
                f"{current_level_score}% "
                f"({round(current_level_score * len(questions) / 100)} of {len(questions)} correct)"
            )
        active_index = section_names.index(active_section)
        next_section = next(
            (
                section_names[index]
                for index in range(active_index + 1, len(section_names))
                if section_names[index] not in st.session_state.objective_submitted
            ),
            None,
        )
        if next_section is None:
            next_section = next(
                (
                    section_name
                    for section_name in section_names
                    if section_name not in st.session_state.objective_submitted
                ),
                None,
            )
        with next_display:
            if next_section is not None:
                next_label = next_section.replace("_test", "").replace("_", " ").title()
                if st.button(f"Next: {next_label} ➜", key=f"next_objective_{active_section}", width="stretch"):
                    st.session_state.objective_active_section = next_section
                    st.rerun()
            elif st.button("Continue to Behavioral Assessment ➜", key="objective_finish_next", width="stretch"):
                st.session_state.completed_stages.add(2)
                st.session_state.current_stage = 3
                st.rerun()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⬅ Back",
            width="stretch"
        ):

            st.session_state.current_stage = 1

            st.rerun()

    with col2:

        if st.button(
            "Continue to Behavioral Assessment ➜",
            type="primary",
            width="stretch"
        ):

            all_scores = st.session_state.answers.get("objective_scores", {})
            missing_sections = [
                name for name in section_names
                if name not in st.session_state.objective_submitted
            ]
            if missing_sections:
                st.warning("Submit each objective submodule first: " + ", ".join(name.replace("_", " ").title() for name in missing_sections))
            else:
                st.session_state.completed_stages.add(2)
                st.session_state.current_stage = 3
                st.rerun()


# ============================================================
# STAGE 3
# ============================================================

elif current_stage == 3:

    st.header(
        "🤝 Behavioral Assessment"
    )

    st.write(
        "Choose the option that best represents you."
    )

    options = [

        "1 - Strongly Disagree",
        "2 - Disagree",
        "3 - Neutral",
        "4 - Agree",
        "5 - Strongly Agree",
    ]

    previous = (
        st.session_state.answers.get(
            "behavioral",
            {}
        )
    )

    behavioral_answers = {}

    for key, questions in (
        BEHAVIORAL_QUESTIONS.items()
    ):

        st.subheader(
            key.replace(
                "_skill",
                ""
            ).replace(
                "_",
                " "
            ).title()
        )

        values = []

        previous_value = previous.get(
            key,
            None
        )

        for i, question in enumerate(
            questions
        ):

            if previous_value in [
                1,
                2,
                3,
                4,
                5
            ]:

                default_index = (
                    previous_value - 1
                )

            else:

                default_index = None

            answer = st.radio(
                question,
                options,
                index=default_index,
                key=f"behavior_{key}_{i}"
            )

            if answer is None:

                values.append(
                    None
                )

            else:

                try:

                    values.append(
                        int(
                            answer.split(
                                " - "
                            )[0]
                        )
                    )

                except Exception:

                    values.append(
                        None
                    )

        behavioral_answers[
            key
        ] = values

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⬅ Back",
            width="stretch"
        ):

            st.session_state.current_stage = 2

            st.rerun()

    with col2:

        if st.button(
            "Continue to Career Interests ➜",
            type="primary",
            width="stretch"
        ):

            invalid = False

            for values in (
                behavioral_answers.values()
            ):

                if any(
                    value is None
                    for value in values
                ):

                    invalid = True

                    break

            if invalid:

                st.warning(
                    "Please answer all behavioral questions."
                )

            else:

                st.session_state.answers[
                    "behavioral_answers"
                ] = behavioral_answers

                st.session_state.answers[
                    "behavioral"
                ] = {

                    key:
                        round(
                            sum(values)
                            /
                            len(values)
                        )

                    for key, values
                    in behavioral_answers.items()
                }

                st.session_state.completed_stages.add(
                    3
                )

                st.session_state.current_stage = 4

                st.rerun()


# ============================================================
# STAGE 4
# ============================================================

elif current_stage == 4:

    st.header(
        "❤️ Career Interests"
    )

    st.write(
        "Tell us how strongly you are interested in each career area."
    )

    options = [

        "1 - Not Interested",
        "2 - Slightly Interested",
        "3 - Neutral",
        "4 - Interested",
        "5 - Highly Interested",
    ]

    previous = (
        st.session_state.answers.get(
            "interests",
            {}
        )
    )

    interest_answers = {}

    for key, questions in (
        INTEREST_QUESTIONS.items()
    ):

        title = key.replace(
            "interest_",
            ""
        ).replace(
            "_",
            " "
        ).title()

        st.subheader(
            title
        )

        values = []

        previous_value = previous.get(
            key,
            None
        )

        for i, question in enumerate(
            questions
        ):

            if previous_value in [
                1,
                2,
                3,
                4,
                5
            ]:

                default_index = (
                    previous_value - 1
                )

            else:

                default_index = None

            answer = st.radio(
                question,
                options,
                index=default_index,
                key=f"interest_{key}_{i}"
            )

            if answer is None:

                values.append(
                    None
                )

            else:

                try:

                    values.append(
                        int(
                            answer.split(
                                " - "
                            )[0]
                        )
                    )

                except Exception:

                    values.append(
                        None
                    )

        interest_answers[
            key
        ] = values

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⬅ Back",
            width="stretch"
        ):

            st.session_state.current_stage = 3

            st.rerun()

    with col2:

        if st.button(
            "🚀 Analyze My Career",
            type="primary",
            width="stretch"
        ):

            invalid = False

            for values in (
                interest_answers.values()
            ):

                if any(
                    value is None
                    for value in values
                ):

                    invalid = True

                    break

            if invalid:

                st.warning(
                    "Please answer all career-interest questions."
                )

            else:

                st.session_state.answers[
                    "interest_answers"
                ] = interest_answers

                st.session_state.answers[
                    "interests"
                ] = {

                    key:
                        round(
                            sum(values)
                            /
                            len(values)
                        )

                    for key, values
                    in interest_answers.items()
                }

                prediction = predict_career()

                if prediction:

                    st.session_state.analysis_result = (
                        prediction
                    )

                    st.session_state.completed_stages.add(
                        4
                    )

                    st.session_state.current_stage = 5

                    st.rerun()

                else:

                    st.error(
                        "Unable to generate career prediction."
                    )


# ============================================================
# STAGE 5
# ============================================================

elif current_stage == 5:

    career = get_valid_career()

    st.header(
        "🎯 Career Prediction"
    )

    if career is None:

        st.warning(
            "Complete the assessment first."
        )

        if st.button(
            "Go to Career Interests",
            type="primary",
            width="stretch"
        ):

            st.session_state.current_stage = 4

            st.rerun()

    else:

        confidence = (
            st.session_state.prediction_confidence
        )

        st.markdown(
            "### Your Personalized Recommendation"
        )

        st.info(
            "Your career match combines self-assessment results (30%) "
            "with objective assessment scores (70%)."
        )

        st.markdown(
            f"""
            <div class="prediction-box">

            <div style="
                color:#64748b;
                font-size:15px;
                font-weight:650;
            ">
            Recommended Career
            </div>

            <div style="
                color:#312e81;
                font-size:38px;
                font-weight:850;
                margin:8px 0;
            ">
            🌟 {career}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if confidence is not None:

            st.metric(
                "Weighted Career Match",
                f"{confidence}%"
            )

        st.divider()

        features = build_feature_vector()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🎓 CGPA",
                f"{features[2]:.1f}"
            )

        with col2:

            st.metric(
                "📊 Assessment Score",
                f"{features[-1]:.1f}%"
            )

        with col3:

            st.metric(
                "🎯 Recommended Role",
                career
            )

        st.divider()

        st.subheader(
            "🧠 Your Career Profile"
        )

        left, right = st.columns(2)

        with left:

            st.info(
                "Technical Profile\n\n"
                "Your technical skills and objective "
                "assessment performance are considered "
                "while generating the recommendation."
            )

        with right:

            st.info(
                "Career Alignment\n\n"
                "Your career interests, behavioral "
                "characteristics and academic profile "
                "contribute to the prediction."
            )

        st.divider()

        st.subheader(
            "💡 Why This Career?"
        )

        role_weights = (
            CAREER_CRITERIA_WEIGHTS.get(
                career,
                {}
            )
        )

        if role_weights:

            for skill, weight in sorted(
                role_weights.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]:

                st.write(
                    f"**{skill}** — {weight}% role importance"
                )

        st.info(
            "Career matching uses 30% self-assessment and 70% objective scores. "
            "The role criteria below show how each skill or attribute contributes "
            "within those two score groups."
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "⬅ Back",
                width="stretch"
            ):

                st.session_state.current_stage = 4

                st.rerun()

        with col2:

            if st.button(
                "View Skill Gap Analysis ➜",
                type="primary",
                width="stretch"
            ):

                st.session_state.completed_stages.add(
                    5
                )

                st.session_state.current_stage = 6

                st.rerun()


# ============================================================
# STAGE 6
# ============================================================

elif current_stage == 6:

    career = get_valid_career()

    st.header(
        "📊 Skill Gap Analysis"
    )

    if career is None:

        st.warning(
            "Career prediction is not available."
        )

    else:

        st.success(
            f"Predicted Career: {career}"
        )

        st.write(
            "The following comparison shows your current "
            "assessed level against the expected level "
            "for your predicted career."
        )

        gaps = calculate_skill_gaps(
            career
        )
        if gaps:

            priority = [

                item
                for item in gaps
                if item["gap"] > 0

            ][:3]

            if priority:

                st.subheader(
                    "🔥 Top Priority Areas"
                )

                columns = st.columns(
                    len(priority)
                )

                for col, item in zip(
                    columns,
                    priority
                ):

                    with col:

                        st.metric(
                            item["skill"],
                            f"{item['gap']:.0f}% gap"
                        )

                st.divider()

            gap_rows = []

            for item in gaps:

                if item["gap"] == 0:

                    status = "🟢 Ready"

                elif item["gap"] <= 15:

                    status = "🟡 Small Gap"

                elif item["gap"] <= 30:

                    status = "🟠 Moderate Gap"

                else:

                    status = "🔴 High Priority"

                gap_rows.append({

                    "Skill":
                        item["skill"],

                    "Current":
                        f"{item['current']:.0f}%",

                    "Required":
                        f"{item['required']:.0f}%",

                    "Gap":
                        f"{item['gap']:.0f}%",

                    "Status":
                        status,
                })

            gap_df = pd.DataFrame(
                gap_rows
            )

            st.dataframe(
                gap_df,
                width="stretch",
                hide_index=True
            )

            st.divider()

            st.subheader(
                "📈 Skill Progress"
            )

            for item in gaps:

                if item["required"] > 0:

                    progress = min(
                        item["current"]
                        /
                        item["required"],
                        1.0
                    )

                else:

                    progress = 0

                st.write(
                    f"**{item['skill']}**"
                )

                st.progress(
                    progress
                )

                st.caption(
                    f"Current: {item['current']:.0f}% "
                    f"• Required: {item['required']:.0f}%"
                )

        st.divider()

        st.subheader(
            "📌 Career Prediction Criteria"
        )

        st.write(
            "The table below shows the project-defined "
            "importance of each criterion for every career role."
        )

        st.info(
            "These role criteria feed the career match, which weights "
            "self-assessment at 30% and objective assessment at 70%."
        )

        all_criteria = sorted(
            set(
                criterion
                for criteria
                in CAREER_CRITERIA_WEIGHTS.values()
                for criterion
                in criteria.keys()
            )
        )

        criteria_rows = []

        for criterion in all_criteria:

            row = {
                "Criterion":
                    criterion
            }

            for role in (
                CAREER_CRITERIA_WEIGHTS.keys()
            ):

                row[role] = (
                    CAREER_CRITERIA_WEIGHTS[
                        role
                    ].get(
                        criterion,
                        0
                    )
                )

            criteria_rows.append(
                row
            )

        total_row = {

            "Criterion":
                "TOTAL"
        }

        for role in (
            CAREER_CRITERIA_WEIGHTS.keys()
        ):

            total_row[role] = sum(
                CAREER_CRITERIA_WEIGHTS[
                    role
                ].values()
            )

        criteria_rows.append(
            total_row
        )

        criteria_df = pd.DataFrame(
            criteria_rows
        )

        st.dataframe(
            criteria_df,
            width="stretch",
            hide_index=True
        )

        st.divider()

        st.subheader(
            f"🎯 {career} — Key Criteria"
        )

        selected_criteria = (
            CAREER_CRITERIA_WEIGHTS.get(
                career,
                {}
            )
        )

        for criterion, weight in sorted(
            selected_criteria.items(),
            key=lambda x: x[1],
            reverse=True
        ):

            st.write(
                f"**{criterion}** — {weight}%"
            )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "⬅ Back",
                width="stretch"
            ):

                st.session_state.current_stage = 5

                st.rerun()

        with col2:

            if st.button(
                "🗺️ Personalized Roadmap ➜",
                type="primary",
                width="stretch"
            ):

                st.session_state.completed_stages.add(
                    6
                )

                st.session_state.current_stage = 7

                st.rerun()


# ============================================================
# STAGE 7
# ============================================================

elif current_stage == 7:

    career = get_valid_career()

    st.header(
        "🗺️ Personalized Roadmap"
    )

    if career is None:

        st.warning(
            "Complete the career prediction first."
        )

    else:

        st.success(
            f"Your recommended path: {career}"
        )

        gaps = calculate_skill_gaps(
            career
        )
        normalized_skill_gaps = {
            " ".join(str(item["skill"]).lower().split()): float(item["gap"])
            for item in gaps
        }

        resource_skill_names = {
            " ".join(resource_name.lower().split())
            for resource_name in LEARNING_RESOURCES
        }
        priority_gaps = sorted(
            (
                item for item in gaps
                if item["gap"] > 0
                and " ".join(str(item["skill"]).lower().split()) in resource_skill_names
            ),
            key=lambda item: item["gap"],
            reverse=True,
        )[:3]

        if priority_gaps:

            st.subheader(
                "🔥 Start With These Skill Gaps"
            )

            columns = st.columns(
                len(priority_gaps)
            )

            for col, item in zip(
                columns,
                priority_gaps
            ):

                with col:

                    st.metric(
                        item["skill"],
                        f"{item['gap']:.0f}% gap"
                    )

            st.divider()

        st.subheader(
            "🚀 Your Learning Path"
        )

        full_roadmap = get_roadmap(career)
        roadmap_by_skill = {
            " ".join(str(item[0]).lower().split()): item
            for item in full_roadmap
        }
        roadmap = []
        for gap_item in priority_gaps:
            normalized_name = " ".join(str(gap_item["skill"]).lower().split())
            roadmap_item = roadmap_by_skill.get(normalized_name)
            if roadmap_item is None:
                resource_match = next(
                    (
                        resource_name
                        for resource_name in LEARNING_RESOURCES
                        if " ".join(resource_name.lower().split()) == normalized_name
                    ),
                    None,
                )
                roadmap_item = (
                    gap_item["skill"],
                    f"Focus on the highest-priority gap ({gap_item['gap']:.0f}%) and practice it with a small project.",
                    resource_match,
                )
            roadmap.append(roadmap_item)

        if not roadmap:
            st.success("No priority skill gaps were found. Keep building projects to strengthen your profile.")

        for index, item in enumerate(
            roadmap,
            start=1
        ):

            skill = item[0]

            description = item[1]

            resource = item[2]

            st.markdown(
                f"### {index}. {skill}"
            )

            st.write(
                description
            )

            if (
                resource
                and
                resource in LEARNING_RESOURCES
            ):

                resource_data = (
                    LEARNING_RESOURCES[
                        resource
                    ]
                )

                with st.expander(
                    f"📚 Explore {resource}"
                ):

                    st.write(
                        resource_data[
                            "description"
                        ]
                    )

                    st.subheader(
                        "📌 Topics to Learn"
                    )
                    st.caption("Checked topics are identified skill gaps. Leave a box empty when you already feel confident in that topic.")

                    topics = (
                        resource_data[
                            "topics"
                        ]
                    )

                    topic_columns = st.columns(
                        2
                    )
                    lacking_topics_in_learning_order = []

                    for i, topic in enumerate(
                        topics
                    ):
                        normalized_resource = " ".join(str(resource or skill).lower().split())
                        resource_gap = normalized_skill_gaps.get(normalized_resource, 0.0)
                        lacks_topic = roadmap_topic_is_lacking(
                            resource,
                            topic,
                            st.session_state.answers.get("objective_answers", {}),
                            st.session_state.objective_submitted,
                            resource_gap,
                            st.session_state.answers.get("skills", {}),
                        )
                        checkbox_key = f"roadmap_topic_v2_{career}_{resource or skill}_{i}"
                        if checkbox_key not in st.session_state:
                            st.session_state[checkbox_key] = lacks_topic
                        if st.session_state[checkbox_key]:
                            lacking_topics_in_learning_order.append(topic)
                        with topic_columns[i % 2]:
                            st.checkbox(topic, key=checkbox_key)

                    st.divider()

                    st.subheader(
                        "🛣️ Recommended Learning Order"
                    )

                    if lacking_topics_in_learning_order:
                        st.caption(
                            "Work through your identified gaps in the same sequence as the topic list, "
                            "so prerequisite concepts come first."
                        )
                        for i, topic in enumerate(
                            lacking_topics_in_learning_order,
                            start=1,
                        ):
                            st.write(f"{i}. {topic}")
                    else:
                        st.success(
                            "No topic gaps are currently selected. Review the checked topic list if you want to update your focus."
                        )

                    st.divider()

                    st.link_button(
                        f"🎥 Learn {resource}",
                        resource_data[
                            "link"
                        ]
                    )

            else:

                st.info(
                    f"Focus on {skill}, practice it regularly "
                    "and build a small project."
                )

            st.divider()

        st.success(
            "🎉 Your personalized career journey is ready!"
        )

        st.write(
            "Follow the roadmap, close your skill gaps, "
            "build projects and prepare for placements."
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "⬅ Back",
                width="stretch"
            ):

                st.session_state.current_stage = 6

                st.rerun()

        with col2:

            if st.button(
                "🔄 Start New Assessment",
                type="primary",
                width="stretch"
            ):

                reset_application()

                st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SKILL TO ROLE • AI-Based Personalized Career Prediction and Skill Assessment System"
)
