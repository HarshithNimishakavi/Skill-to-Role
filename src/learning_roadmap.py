import sys
import os

# ============================================================
# PROJECT ROOT
# ============================================================

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


# ============================================================
# VIDEO RESOURCES FOR EACH SKILL
# ============================================================

VIDEO_RESOURCES = {

    "python_skill": {
        "title": "Python Tutorials",
        "channel": "Corey Schafer",
        "video": "https://www.youtube.com/playlist?list=PL-osiE80TeTsqhIuOqKhwl9DLd6aW8v9i"
    },

    "ml_skill": {
        "title": "Machine Learning Playlist",
        "channel": "StatQuest with Josh Starmer",
        "video": "https://www.youtube.com/playlist?list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF"
    },

    "dsa_skill": {
        "title": "Striver's A2Z DSA Course",
        "channel": "take U forward",
        "video": "https://www.youtube.com/playlist?list=PLgUwDviBIf0oF6QL8m22w1hIDC1vJ_BHz"
    },

    "sql_skill": {
        "title": "Data Analyst Bootcamp - SQL",
        "channel": "Alex The Analyst",
        "video": "https://www.youtube.com/watch?v=cnjhHZNJEDk"
    },

    "data_analysis_skill": {
        "title": "Data Analyst Bootcamp",
        "channel": "Alex The Analyst",
        "video": "https://www.youtube.com/watch?v=cnjhHZNJEDk"
    },

    "web_development_skill": {
        "title": "Full Stack Web Development Course",
        "channel": "freeCodeCamp",
        "video": "https://www.youtube.com/watch?v=nu_pCVPKzTk"
    },

    "cybersecurity_skill": {
        "title": "Cybersecurity Roadmap",
        "channel": "NetworkChuck",
        "video": "https://www.youtube.com/watch?v=5xWnmUEi1Qw"
    },

    "aptitude_score": {
        "title": "Quantitative Aptitude for Placements",
        "channel": "Placement Preparation",
        "video": "https://www.youtube.com/results?search_query=quantitative+aptitude+placement+preparation"
    },

    "reasoning_score": {
        "title": "Logical Reasoning for Placements",
        "channel": "Placement Preparation",
        "video": "https://www.youtube.com/results?search_query=logical+reasoning+placement+preparation"
    },

    "communication_skill": {
        "title": "Communication Skills for Interviews",
        "channel": "Interview Preparation",
        "video": "https://www.youtube.com/results?search_query=communication+skills+for+interviews"
    },

    "problem_solving_skill": {
        "title": "Problem Solving and Critical Thinking",
        "channel": "Career Skills",
        "video": "https://www.youtube.com/results?search_query=problem+solving+critical+thinking"
    },

    "adaptability_skill": {
        "title": "Adaptability and Learning Skills",
        "channel": "Career Skills",
        "video": "https://www.youtube.com/results?search_query=adaptability+learning+skills"
    }
}


# ============================================================
# CAREER-SPECIFIC ROADMAP
# ============================================================

LEARNING_ROADMAP = {

    # --------------------------------------------------------
    # MACHINE LEARNING ENGINEER
    # --------------------------------------------------------

    "Machine Learning Engineer": {

        "ml_skill": [
            "Machine Learning fundamentals",
            "Data preprocessing",
            "Supervised learning",
            "Unsupervised learning",
            "Model evaluation",
            "Feature engineering",
            "Hyperparameter tuning",
            "Build ML projects"
        ],

        "python_skill": [
            "Python fundamentals",
            "Functions and modules",
            "Object-oriented programming",
            "NumPy",
            "Pandas",
            "Exception handling",
            "Python problem solving"
        ],

        "dsa_skill": [
            "Arrays",
            "Strings",
            "Linked Lists",
            "Stacks and Queues",
            "Trees",
            "Graphs",
            "Searching and Sorting",
            "Practice coding problems"
        ],

        "sql_skill": [
            "SQL fundamentals",
            "Joins",
            "Subqueries",
            "Window functions",
            "Query optimization"
        ],

        "data_analysis_skill": [
            "Data cleaning",
            "Pandas",
            "NumPy",
            "EDA",
            "Data visualization"
        ],

        "problem_solving_skill": [
            "Coding problems",
            "Algorithmic thinking",
            "Logical problem solving",
            "Real-world ML problems"
        ]
    },


    # --------------------------------------------------------
    # DATA SCIENTIST
    # --------------------------------------------------------

    "Data Scientist": {

        "python_skill": [
            "Python fundamentals",
            "NumPy",
            "Pandas",
            "Data manipulation",
            "Python problem solving"
        ],

        "sql_skill": [
            "SQL fundamentals",
            "Joins",
            "Subqueries",
            "Window functions"
        ],

        "ml_skill": [
            "Machine Learning fundamentals",
            "Supervised learning",
            "Unsupervised learning",
            "Model evaluation",
            "Feature engineering"
        ],

        "data_analysis_skill": [
            "EDA",
            "Data cleaning",
            "Data visualization",
            "Pandas",
            "Statistical analysis"
        ],

        "problem_solving_skill": [
            "Logical problem solving",
            "Analytical thinking",
            "Data science case studies"
        ],

        "aptitude_score": [
            "Percentages",
            "Ratios",
            "Averages",
            "Probability basics",
            "Quantitative aptitude"
        ]
    },


    # --------------------------------------------------------
    # DATA ANALYST
    # --------------------------------------------------------

    "Data Analyst": {

        "sql_skill": [
            "SQL fundamentals",
            "Joins",
            "Subqueries",
            "GROUP BY",
            "Window functions"
        ],

        "data_analysis_skill": [
            "Data cleaning",
            "Pandas",
            "EDA",
            "Data visualization",
            "Dashboard development"
        ],

        "python_skill": [
            "Python fundamentals",
            "NumPy",
            "Pandas",
            "Data manipulation"
        ],

        "communication_skill": [
            "Data storytelling",
            "Presentation skills",
            "Explaining insights",
            "Technical communication"
        ],

        "problem_solving_skill": [
            "Analytical thinking",
            "Business problem solving",
            "Case-study practice"
        ],

        "aptitude_score": [
            "Percentages",
            "Ratios",
            "Averages",
            "Data interpretation"
        ]
    },


    # --------------------------------------------------------
    # SOFTWARE DEVELOPER
    # --------------------------------------------------------

    "Software Developer": {

        "dsa_skill": [
            "Arrays",
            "Strings",
            "Linked Lists",
            "Stacks and Queues",
            "Trees",
            "Graphs",
            "Searching and Sorting",
            "Dynamic Programming"
        ],

        "python_skill": [
            "Python fundamentals",
            "OOP",
            "Functions",
            "Exception handling",
            "File handling"
        ],

        "problem_solving_skill": [
            "Coding problems",
            "Algorithmic thinking",
            "Competitive programming practice"
        ],

        "communication_skill": [
            "Technical communication",
            "Interview communication",
            "Team collaboration"
        ],

        "adaptability_skill": [
            "Learning new technologies",
            "Exploring development frameworks",
            "Working with new technologies"
        ]
    },


    # --------------------------------------------------------
    # WEB DEVELOPER
    # --------------------------------------------------------

    "Web Developer": {

        "web_development_skill": [
            "HTML",
            "CSS",
            "JavaScript",
            "DOM",
            "APIs",
            "Frontend development",
            "Backend fundamentals",
            "Build web projects"
        ],

        "python_skill": [
            "Python fundamentals",
            "Functions",
            "OOP",
            "Backend development"
        ],

        "sql_skill": [
            "SQL fundamentals",
            "CRUD operations",
            "Joins",
            "Database design"
        ],

        "dsa_skill": [
            "Arrays",
            "Strings",
            "Stacks",
            "Queues",
            "Basic algorithms"
        ],

        "problem_solving_skill": [
            "Debugging",
            "Logical thinking",
            "Problem-solving practice"
        ]
    },


    # --------------------------------------------------------
    # CYBERSECURITY ANALYST
    # --------------------------------------------------------

    "Cybersecurity Analyst": {

        "cybersecurity_skill": [
            "Networking fundamentals",
            "Cybersecurity fundamentals",
            "Authentication",
            "Cryptography basics",
            "Web security",
            "Vulnerability assessment",
            "Security monitoring",
            "Incident response"
        ],

        "python_skill": [
            "Python fundamentals",
            "Python scripting",
            "Automation",
            "File handling"
        ],

        "sql_skill": [
            "SQL fundamentals",
            "Database security",
            "SQL injection concepts"
        ],

        "dsa_skill": [
            "Arrays",
            "Strings",
            "Basic data structures",
            "Basic algorithms"
        ],

        "problem_solving_skill": [
            "Logical reasoning",
            "Threat analysis",
            "Security problem solving"
        ],

        "reasoning_score": [
            "Logical reasoning",
            "Analytical reasoning",
            "Pattern recognition",
            "Problem-solving practice"
        ]
    }
}


# ============================================================
# GENERATE ROADMAP
# ============================================================

def generate_learning_roadmap(predicted_career, skill_gaps):

    if predicted_career not in LEARNING_ROADMAP:
        raise ValueError(
            f"No roadmap available for {predicted_career}"
        )

    career_roadmap = LEARNING_ROADMAP[predicted_career]

    roadmap = []

    # Sort gaps from highest to lowest
    sorted_gaps = sorted(
        skill_gaps,
        key=lambda x: x["gap"],
        reverse=True
    )

    for gap in sorted_gaps:

        skill = gap["skill"]
        gap_value = gap["gap"]

        # Ignore skills that do not need improvement
        if gap_value <= 0:
            continue

        # Get topics
        topics = career_roadmap.get(
            skill,
            [
                f"Improve {skill}",
                "Practice regularly",
                "Build practical projects"
            ]
        )

        # Get video
        video_resource = VIDEO_RESOURCES.get(skill)

        if video_resource:

            video_title = video_resource["title"]
            video_channel = video_resource["channel"]
            video_link = video_resource["video"]

        else:

            video_title = "No specific resource available"
            video_channel = ""
            video_link = ""

        roadmap.append({

            "priority": len(roadmap) + 1,

            "skill": skill,

            "current_score": gap["current_score"],

            "required_score": gap["required_score"],

            "gap": gap_value,

            "topics": topics,

            "video_title": video_title,

            "video_channel": video_channel,

            "video_link": video_link
        })

    return roadmap


# ============================================================
# DISPLAY ROADMAP
# ============================================================

def display_roadmap(predicted_career, roadmap):

    print("\n")

    print("=" * 70)

    print("PERSONALIZED LEARNING ROADMAP")

    print("=" * 70)

    print(
        f"\nTarget Career: {predicted_career}"
    )

    # --------------------------------------------------------
    # IF NO SKILL GAP
    # --------------------------------------------------------

    if not roadmap:

        print(
            "\nExcellent! No major skill gaps were detected."
        )

        print("=" * 70)

        return

    # --------------------------------------------------------
    # DISPLAY EACH PRIORITY
    # --------------------------------------------------------

    for item in roadmap:

        print("\n")

        print("-" * 70)

        print(
            f"Priority {item['priority']}: "
            f"{item['skill']}"
        )

        print(
            f"Current Score : {item['current_score']}"
        )

        print(
            f"Required Score: {item['required_score']}"
        )

        print(
            f"Skill Gap     : {item['gap']} points"
        )

        # ----------------------------------------------------
        # TOPICS
        # ----------------------------------------------------

        print("\nRecommended Topics:")

        for number, topic in enumerate(
            item["topics"],
            start=1
        ):

            print(
                f"  {number}. {topic}"
            )

        # ----------------------------------------------------
        # VIDEO
        # ----------------------------------------------------

        print("\nRecommended Video:")

        print(
            f"  Title   : {item['video_title']}"
        )

        print(
            f"  Channel : {item['video_channel']}"
        )

        print(
            f"  Link    : {item['video_link']}"
        )

    print("\n")

    print("=" * 70)

    print(
        "Personalized roadmap generated successfully."
    )

    print("=" * 70)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    # Example predicted career
    predicted_career = "Machine Learning Engineer"

    # Example skill-gap output
    skill_gaps = [

        {
            "skill": "ml_skill",
            "current_score": 70,
            "required_score": 85,
            "gap": 15,
            "status": "Needs Improvement"
        },

        {
            "skill": "python_skill",
            "current_score": 70,
            "required_score": 80,
            "gap": 10,
            "status": "Needs Improvement"
        },

        {
            "skill": "dsa_skill",
            "current_score": 70,
            "required_score": 75,
            "gap": 5,
            "status": "Needs Improvement"
        },

        {
            "skill": "sql_skill",
            "current_score": 90,
            "required_score": 70,
            "gap": 0,
            "status": "Good"
        },

        {
            "skill": "data_analysis_skill",
            "current_score": 70,
            "required_score": 70,
            "gap": 0,
            "status": "Good"
        },

        {
            "skill": "problem_solving_skill",
            "current_score": 90,
            "required_score": 75,
            "gap": 0,
            "status": "Good"
        }
    ]

    # Generate roadmap
    roadmap = generate_learning_roadmap(
        predicted_career,
        skill_gaps
    )

    # Display roadmap
    display_roadmap(
        predicted_career,
        roadmap
    )