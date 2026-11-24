# ============================================================
# SKILL TO ROLE - ASSESSMENT QUESTION BANK
# ============================================================
# Order:
# 1. Basic Information
# 2. Skill Assessment (Beginner / Intermediate / Advanced)
# 3. Objective Assessment (5 questions per skill)
# 4. Behavioral Assessment
# 5. Career Interest Assessment
#
# Objective questions contain answer keys.
# Skill, behavioral and interest questions have no right/wrong answer.
# ============================================================


# ============================================================
# 1. BASIC INFORMATION
# ============================================================

BASIC_INFO = {
    "age": {
        "label": "Enter your age",
        "type": "number",
        "min": 18,
        "max": 30
    },

    "year_of_study": {
        "label": "Select your current year of study",
        "type": "select",
        "options": [1, 2, 3, 4]
    },

    "cgpa": {
        "label": "Enter your current CGPA",
        "type": "number",
        "min": 0,
        "max": 10,
        "step": 0.01
    }
}


# ============================================================
# 2. SKILL ASSESSMENT
# ============================================================
# The student selects the highest level whose listed topics
# they can understand and perform comfortably.
#
# Scoring can be handled in assessment_scoring.py.
# Suggested mapping:
# Beginner = 40
# Intermediate = 70
# Advanced = 90
# ============================================================

SKILL_ASSESSMENT = {

    "python_skill": {
        "title": "Python",
        "instruction": "Select the highest level whose topics you can comfortably understand and use.",

        "levels": {
            "Beginner": [
                "Variables and data types",
                "if/else conditions",
                "for and while loops",
                "Lists, tuples, sets and dictionaries",
                "Basic functions and input/output"
            ],

            "Intermediate": [
                "List and dictionary comprehensions",
                "Exception handling",
                "File handling",
                "Modules and packages",
                "Object-oriented programming basics",
                "NumPy and Pandas basics"
            ],

            "Advanced": [
                "Advanced object-oriented programming",
                "Decorators and generators",
                "Iterators and context managers",
                "Efficient data structures and algorithms",
                "Writing modular and optimized Python applications"
            ]
        }
    },


    "sql_skill": {
        "title": "SQL",
        "instruction": "Select the highest level whose topics you can comfortably understand and use.",

        "levels": {
            "Beginner": [
                "SELECT and FROM",
                "WHERE conditions",
                "ORDER BY",
                "DISTINCT",
                "Basic aggregate functions such as COUNT, SUM and AVG"
            ],

            "Intermediate": [
                "INNER JOIN and OUTER JOIN",
                "GROUP BY and HAVING",
                "Subqueries",
                "CASE statements",
                "Working with multiple related tables"
            ],

            "Advanced": [
                "Common Table Expressions (CTEs)",
                "Window functions",
                "Complex nested queries",
                "Query optimization concepts",
                "Indexes and execution-plan concepts"
            ]
        }
    },


    "ml_skill": {
        "title": "Machine Learning",
        "instruction": "Select the highest level whose topics you can comfortably understand and use.",

        "levels": {
            "Beginner": [
                "What machine learning is",
                "Supervised and unsupervised learning",
                "Classification and regression",
                "Basic algorithms such as Linear Regression, Logistic Regression and KNN",
                "Basic model evaluation concepts"
            ],

            "Intermediate": [
                "Data preprocessing",
                "Feature engineering",
                "Decision Trees and Random Forest",
                "SVM and Naive Bayes",
                "Confusion matrix, precision, recall and F1-score",
                "Hyperparameter tuning basics"
            ],

            "Advanced": [
                "ML pipelines",
                "Cross-validation and advanced model tuning",
                "Ensemble learning",
                "Handling class imbalance and model-selection strategies",
                "Model deployment and monitoring concepts"
            ]
        }
    },


    "data_analysis_skill": {
        "title": "Data Analysis",
        "instruction": "Select the highest level whose topics you can comfortably understand and use.",

        "levels": {
            "Beginner": [
                "Basic Excel operations",
                "Reading datasets",
                "Basic data cleaning",
                "Basic Pandas operations",
                "Simple charts and graphs"
            ],

            "Intermediate": [
                "Data cleaning and missing-value handling",
                "Pandas-based EDA",
                "Grouping and aggregation",
                "Data visualization",
                "Finding patterns and relationships in data"
            ],

            "Advanced": [
                "Advanced exploratory data analysis",
                "Feature and variable analysis",
                "Advanced visualization and dashboards",
                "Automating data-analysis workflows",
                "Communicating analytical findings for decision-making"
            ]
        }
    },


    "web_development_skill": {
        "title": "Web Development",
        "instruction": "Select the highest level whose topics you can comfortably understand and use.",

        "levels": {
            "Beginner": [
                "HTML basics",
                "CSS basics",
                "Basic JavaScript",
                "Forms and page structure",
                "Basic responsive design"
            ],

            "Intermediate": [
                "JavaScript DOM manipulation",
                "Responsive web design",
                "Frontend frameworks or libraries",
                "REST APIs",
                "Backend fundamentals and database integration"
            ],

            "Advanced": [
                "Full-stack application development",
                "Authentication and authorization",
                "API architecture",
                "Application security concepts",
                "Deployment and scalable application design"
            ]
        }
    },


    "cybersecurity_skill": {
        "title": "Cybersecurity",
        "instruction": "Select the highest level whose topics you can comfortably understand and use.",

        "levels": {
            "Beginner": [
                "Basic cybersecurity concepts",
                "Common cyber threats",
                "Password and account security",
                "Basic network security",
                "Malware and phishing awareness"
            ],

            "Intermediate": [
                "Authentication and authorization",
                "Network security concepts",
                "Common web vulnerabilities",
                "Security monitoring basics",
                "Secure configuration practices"
            ],

            "Advanced": [
                "Security architecture concepts",
                "Vulnerability assessment concepts",
                "Incident response concepts",
                "Advanced authentication and access control",
                "Security risk analysis"
            ]
        }
    },


    "dsa_skill": {
        "title": "Data Structures and Algorithms",
        "instruction": "Select the highest level whose topics you can comfortably understand and use.",

        "levels": {
            "Beginner": [
                "Arrays and strings",
                "Basic searching",
                "Basic sorting",
                "Stacks and queues",
                "Basic time-complexity concepts"
            ],

            "Intermediate": [
                "Linked lists",
                "Hash tables",
                "Trees and binary search trees",
                "Recursion",
                "Common sorting and searching algorithms",
                "Time and space complexity analysis"
            ],

            "Advanced": [
                "Graphs and graph algorithms",
                "Dynamic programming",
                "Greedy algorithms",
                "Advanced tree concepts",
                "Algorithm optimization and complexity analysis"
            ]
        }
    }
}


# ============================================================
# 3. OBJECTIVE ASSESSMENT
# ============================================================
# Exactly 5 questions per technical skill.
# Each question has one correct answer.
# ============================================================

OBJECTIVE_ASSESSMENT ={

    # --------------------------------------------------------
    # PYTHON - 5 QUESTIONS
    # --------------------------------------------------------
    "python_test": [
        {
            "question": "What is the output of this code?\n\nx = [1, 2, 3]\ny = x\ny.append(4)\nprint(x)",
            "options": [
                "[1, 2, 3]",
                "[1, 2, 3, 4]",
                "[4, 1, 2, 3]",
                "Error"
            ],
            "answer": "[1, 2, 3, 4]"
        },
        {
            "question": "What is the output of this code?\n\nnums = [1, 2, 3, 4]\nresult = [x * 2 for x in nums if x % 2 == 0]\nprint(result)",
            "options": [
                "[2, 4]",
                "[4, 8]",
                "[1, 3]",
                "[2, 4, 6, 8]"
            ],
            "answer": "[4, 8]"
        },
        {
            "question": "What happens here?\n\na = [1, 2]\nb = a.copy()\nb.append(3)\nprint(a, b)",
            "options": [
                "[1, 2, 3] [1, 2, 3]",
                "[1, 2] [1, 2, 3]",
                "[1, 2, 3] [1, 2]",
                "Error"
            ],
            "answer": "[1, 2] [1, 2, 3]"
        },
        {
            "question": "What is the output?\n\nd = {'a': 10, 'b': 20}\nprint(d.get('c', 0))",
            "options": [
                "None",
                "0",
                "Error",
                "'c'"
            ],
            "answer": "0"
        },
        {
            "question": "What is the output?\n\ndef calculate(a, b=5):\n    return a * b\n\nprint(calculate(4))",
            "options": [
                "9",
                "20",
                "25",
                "Error"
            ],
            "answer": "20"
        }
    ],


    # --------------------------------------------------------
    # SQL - 5 QUESTIONS
    # --------------------------------------------------------
    "sql_test": [
        {
            "question": "Which query correctly returns departments whose average salary is greater than 60000?",
            "options": [
                "SELECT department FROM employees WHERE AVG(salary) > 60000 GROUP BY department;",
                "SELECT department FROM employees GROUP BY department HAVING AVG(salary) > 60000;",
                "SELECT department FROM employees HAVING AVG(salary) > 60000;",
                "SELECT department FROM employees WHERE salary > 60000;"
            ],
            "answer": "SELECT department FROM employees GROUP BY department HAVING AVG(salary) > 60000;"
        },
        {
            "question": "Which query returns employees whose salary is greater than the average salary of all employees?",
            "options": [
                "SELECT * FROM employees WHERE salary > AVG(salary);",
                "SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);",
                "SELECT * FROM employees HAVING salary > AVG(salary);",
                "SELECT * FROM employees WHERE AVG(salary) < salary;"
            ],
            "answer": "SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);"
        },
        {
            "question": "Which query returns the second-highest distinct salary?",
            "options": [
                "SELECT MAX(salary) FROM employees;",
                "SELECT MIN(salary) FROM employees;",
                "SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);",
                "SELECT salary FROM employees ORDER BY salary ASC LIMIT 2;"
            ],
            "answer": "SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);"
        },
        {
            "question": "Which condition correctly checks whether a column contains NULL?",
            "options": [
                "WHERE column = NULL",
                "WHERE column == NULL",
                "WHERE column IS NULL",
                "WHERE column != NULL"
            ],
            "answer": "WHERE column IS NULL"
        },
        {
            "question": "Which clause is used to filter groups after GROUP BY?",
            "options": [
                "WHERE",
                "ORDER BY",
                "HAVING",
                "DISTINCT"
            ],
            "answer": "HAVING"
        }
    ],


    # --------------------------------------------------------
    # MACHINE LEARNING - 5 QUESTIONS
    # --------------------------------------------------------
    "ml_test": [
        {
            "question": "Why should a StandardScaler normally be fitted only on the training data?",
            "options": [
                "To increase the dataset size",
                "To avoid data leakage from the test set",
                "To remove the target column",
                "To increase the number of features"
            ],
            "answer": "To avoid data leakage from the test set"
        },
        {
            "question": "A classifier correctly identifies 40 positive samples out of 50 samples predicted as positive. What is its precision?",
            "options": [
                "60%",
                "70%",
                "80%",
                "90%"
            ],
            "answer": "80%"
        },
        {
            "question": "A classifier correctly identifies 75 positive samples out of 100 actual positive samples. What is its recall?",
            "options": [
                "25%",
                "50%",
                "75%",
                "80%"
            ],
            "answer": "75%"
        },
        {
            "question": "A model gets 100% training accuracy but only 68% test accuracy. What is the most likely problem?",
            "options": [
                "Underfitting",
                "Overfitting",
                "Data normalization",
                "Feature scaling"
            ],
            "answer": "Overfitting"
        },
        {
            "question": "Why is feature scaling important for KNN?",
            "options": [
                "KNN uses decision trees",
                "KNN is based on distance calculations",
                "KNN only works with categorical data",
                "Scaling increases the number of classes"
            ],
            "answer": "KNN is based on distance calculations"
        }
    ],


    # --------------------------------------------------------
    # DATA ANALYSIS - 5 QUESTIONS
    # --------------------------------------------------------
    "data_analysis_test": [
        {
            "question": "Which Pandas function is commonly used to identify missing values?",
            "options": [
                "df.isnull()",
                "df.sort()",
                "df.rename()",
                "df.merge()"
            ],
            "answer": "df.isnull()"
        },
        {
            "question": "Which Pandas function is commonly used to group data and calculate aggregates?",
            "options": [
                "groupby()",
                "reshape()",
                "append()",
                "astype()"
            ],
            "answer": "groupby()"
        },
        {
            "question": "Which visualization is generally suitable for showing the distribution of a numerical variable?",
            "options": [
                "Histogram",
                "Pie chart only",
                "Network diagram",
                "Flowchart"
            ],
            "answer": "Histogram"
        },
        {
            "question": "What is the main purpose of exploratory data analysis (EDA)?",
            "options": [
                "To understand patterns, distributions and relationships in data",
                "To deploy an application",
                "To encrypt a database",
                "To replace all missing values with zero automatically"
            ],
            "answer": "To understand patterns, distributions and relationships in data"
        },
        {
            "question": "Which Pandas method combines two DataFrames using matching columns or keys?",
            "options": [
                "merge()",
                "describe()",
                "dropna()",
                "value_counts()"
            ],
            "answer": "merge()"
        }
    ],


    # --------------------------------------------------------
    # WEB DEVELOPMENT - 5 QUESTIONS
    # --------------------------------------------------------
    "web_development_test": [
        {
            "question": "Which HTML element is used to create a hyperlink?",
            "options": [
                "<link>",
                "<a>",
                "<href>",
                "<url>"
            ],
            "answer": "<a>"
        },
        {
            "question": "Which CSS property is commonly used to change the text color?",
            "options": [
                "font-style",
                "background",
                "color",
                "text-decoration"
            ],
            "answer": "color"
        },
        {
            "question": "Which JavaScript method converts a JSON string into a JavaScript object?",
            "options": [
                "JSON.parse()",
                "JSON.stringify()",
                "JSON.object()",
                "JSON.convert()"
            ],
            "answer": "JSON.parse()"
        },
        {
            "question": "What is the main purpose of a REST API?",
            "options": [
                "To define a way for applications to communicate over HTTP",
                "To replace HTML",
                "To compile JavaScript into machine code",
                "To store passwords directly in the browser"
            ],
            "answer": "To define a way for applications to communicate over HTTP"
        },
        {
            "question": "Which HTTP method is commonly used to create a new resource?",
            "options": [
                "GET",
                "POST",
                "DELETE",
                "HEAD"
            ],
            "answer": "POST"
        }
    ],


    # --------------------------------------------------------
    # CYBERSECURITY - 5 QUESTIONS
    # --------------------------------------------------------
    "cybersecurity_test": [
        {
            "question": "Which attack attempts to trick users into revealing sensitive information through fake messages or websites?",
            "options": [
                "Phishing",
                "Hashing",
                "Compression",
                "Load balancing"
            ],
            "answer": "Phishing"
        },
        {
            "question": "What is the main purpose of hashing passwords?",
            "options": [
                "To store passwords in a reversible plain-text format",
                "To create a one-way representation of the password",
                "To increase internet speed",
                "To remove authentication"
            ],
            "answer": "To create a one-way representation of the password"
        },
        {
            "question": "Which vulnerability occurs when untrusted input is inserted into a database query?",
            "options": [
                "SQL Injection",
                "DDoS",
                "Phishing",
                "Shoulder surfing"
            ],
            "answer": "SQL Injection"
        },
        {
            "question": "What is authentication primarily concerned with?",
            "options": [
                "Determining what a user is allowed to access",
                "Verifying the identity of a user",
                "Encrypting every database column",
                "Increasing CPU performance"
            ],
            "answer": "Verifying the identity of a user"
        },
        {
            "question": "What is authorization primarily concerned with?",
            "options": [
                "Verifying a user's identity",
                "Determining what an authenticated user is allowed to access",
                "Creating a password hash",
                "Detecting malware automatically"
            ],
            "answer": "Determining what an authenticated user is allowed to access"
        }
    ],


    # --------------------------------------------------------
    # DSA - 5 QUESTIONS
    # --------------------------------------------------------
    "dsa_test": [
        {
            "question": "Which data structure follows the Last-In-First-Out (LIFO) principle?",
            "options": [
                "Queue",
                "Stack",
                "Linked List",
                "Graph"
            ],
            "answer": "Stack"
        },
        {
            "question": "What is the average-case time complexity of searching for a key in a well-designed hash table?",
            "options": [
                "O(1)",
                "O(log n)",
                "O(n)",
                "O(n log n)"
            ],
            "answer": "O(1)"
        },
        {
            "question": "Which traversal of a Binary Search Tree produces values in sorted order?",
            "options": [
                "Preorder",
                "Postorder",
                "Inorder",
                "Level order"
            ],
            "answer": "Inorder"
        },
        {
            "question": "Which algorithm is commonly used to find the shortest paths from a source vertex in a graph with non-negative edge weights?",
            "options": [
                "Dijkstra's algorithm",
                "Binary Search",
                "Merge Sort",
                "Depth-first search only"
            ],
            "answer": "Dijkstra's algorithm"
        },
        {
            "question": "What is the time complexity of binary search on a sorted array?",
            "options": [
                "O(1)",
                "O(log n)",
                "O(n)",
                "O(n^2)"
            ],
            "answer": "O(log n)"
        }
    ],

    # --------------------------------------------------------
    # APTITUDE - 5 QUESTIONS
    # --------------------------------------------------------
    "aptitude_test": [
        {
            "question": "A can complete a job in 12 days and B can complete it in 18 days. How many days will they take together?",
            "options": [
                "6 days",
                "7.2 days",
                "8 days",
                "9 days"
            ],
            "answer": "7.2 days"
        },
        {
            "question": "A product's price increases from ₹800 to ₹920. What is the percentage increase?",
            "options": [
                "10%",
                "12%",
                "15%",
                "20%"
            ],
            "answer": "15%"
        },
        {
            "question": "The average of five numbers is 24. Four of the numbers are 20, 22, 26 and 28. What is the fifth number?",
            "options": [
                "20",
                "22",
                "24",
                "26"
            ],
            "answer": "24"
        },
        {
            "question": "A person travels 60 km at 30 km/h and another 60 km at 60 km/h. What is the average speed for the entire journey?",
            "options": [
                "35 km/h",
                "40 km/h",
                "45 km/h",
                "50 km/h"
            ],
            "answer": "40 km/h"
        },
        {
            "question": "A value is increased by 20% and then decreased by 10%. What is the overall percentage change?",
            "options": [
                "8% increase",
                "10% increase",
                "8% decrease",
                "10% decrease"
            ],
            "answer": "8% increase"
        }
    ],

    # --------------------------------------------------------
    # REASONING - 5 QUESTIONS
    # --------------------------------------------------------
    "reasoning_test": [
        {
            "question": "Find the next number: 3, 8, 15, 24, 35, ?",
            "options": [
                "42",
                "46",
                "48",
                "50"
            ],
            "answer": "48"
        },
        {
            "question": "If CAT is coded as DBU, how is DOG coded using the same pattern?",
            "options": [
                "EPH",
                "EOG",
                "FPH",
                "DPE"
            ],
            "answer": "EPH"
        },
        {
            "question": "All Machine Learning Engineers know Python. Ravi is a Machine Learning Engineer. What can be concluded?",
            "options": [
                "Ravi knows Python",
                "Ravi does not know Python",
                "Ravi may not be an engineer",
                "Nothing can be concluded"
            ],
            "answer": "Ravi knows Python"
        },
        {
            "question": "Find the next number: 4, 9, 19, 39, 79, ?",
            "options": [
                "149",
                "159",
                "169",
                "179"
            ],
            "answer": "159"
        },
        {
            "question": "A is taller than B. B is taller than C. C is taller than D. Who is the shortest?",
            "options": [
                "A",
                "B",
                "C",
                "D"
            ],
            "answer": "D"
        }
    ]
}


# Each objective module covers five topics, with two questions per topic.
# A question spec is: (prompt, correct answer, three distractors).
OBJECTIVE_TOPIC_BANK = {
    "python_test": [
        ("Lists", [
            ("Which list method adds one item to the end?", "append()", "add()", "push()", "insert_end()"),
            ("What does values[1:3] return for [10, 20, 30, 40]?", "[20, 30]", "[10, 20, 30]", "[20, 30, 40]", "[30, 40]"),
        ]),
        ("Tuples", [
            ("Which statement about a tuple is true?", "Its items cannot be reassigned", "It can only store numbers", "It automatically sorts items", "It is always empty"),
            ("How do you write a one-item tuple containing 7?", "(7,)", "(7)", "[7]", "tuple(7)"),
        ]),
        ("Dictionaries", [
            ("Which expression safely returns a missing key as None?", "record.get('city')", "record['city']", "record.find('city')", "record.value('city')"),
            ("Which method returns a dictionary's key-value pairs?", "items()", "keys_only()", "values()", "pairs()"),
        ]),
        ("Conditionals", [
            ("Which keyword checks another condition after an if?", "elif", "otherwise", "elseif", "when"),
            ("What is printed by: if 3 > 5: print('A') else: print('B')?", "B", "A", "A B", "Nothing"),
        ]),
        ("Loops", [
            ("Which loop is best suited to visit every item in a list?", "for", "switch", "if", "try"),
            ("What does break do inside a loop?", "Stops the loop immediately", "Skips only the current iteration", "Restarts the loop", "Pauses the program"),
        ]),
    ],
    "sql_test": [
        ("SELECT and filtering", [
            ("Which clause filters individual rows?", "WHERE", "HAVING", "GROUP BY", "ORDER BY"),
            ("Which query selects only name from employees?", "SELECT name FROM employees", "GET name IN employees", "SELECT employees.name ALL", "SHOW employees.name"),
        ]),
        ("Aggregation", [
            ("Which function counts rows?", "COUNT(*)", "SUM(*)", "TOTAL ROWS()", "NUMBER(*)"),
            ("Which clause filters grouped results?", "HAVING", "WHERE", "FROM", "LIMIT"),
        ]),
        ("Joins", [
            ("Which join keeps every row from the left table?", "LEFT JOIN", "INNER JOIN", "CROSS JOIN", "RIGHT EXCLUDE"),
            ("What does an INNER JOIN return?", "Rows with matching join values in both tables", "Every row from the left table", "Every possible row combination", "Only unmatched rows"),
        ]),
        ("Subqueries", [
            ("Where can a scalar subquery be used to compare a salary to the average?", "In a WHERE comparison", "Only after ORDER BY", "Only as a table name", "Inside CREATE DATABASE"),
            ("What does IN (SELECT ...) commonly test?", "Whether a value appears in the subquery result", "Whether a table exists", "Whether a column is numeric", "Whether rows are sorted"),
        ]),
        ("NULL and ordering", [
            ("How do you test for a NULL value?", "IS NULL", "= NULL", "== NULL", "EQUALS NULL"),
            ("Which clause sorts query results?", "ORDER BY", "GROUP BY", "HAVING", "WHERE"),
        ]),
    ],
    "ml_test": [
        ("Learning types", [
            ("A model learns from labeled examples. Which approach is this?", "Supervised learning", "Unsupervised learning", "Reinforcement only", "Rule-free clustering"),
            ("Grouping customers without labels is an example of?", "Unsupervised learning", "Supervised learning", "Regression with labels", "Classification with targets"),
        ]),
        ("Preprocessing", [
            ("Why split data into training and test sets?", "To estimate performance on unseen data", "To duplicate every row", "To remove all features", "To guarantee perfect accuracy"),
            ("When should a scaler be fitted?", "On training data only", "On the test set only", "After using test labels", "Separately on each prediction"),
        ]),
        ("Evaluation", [
            ("Precision is the proportion of predicted positives that are?", "Actually positive", "Actually negative", "All observations", "Missing labels"),
            ("Recall measures the proportion of actual positives that are?", "Correctly identified", "Predicted negative", "Removed during cleaning", "Correctly ranked only"),
        ]),
        ("Overfitting", [
            ("High training score and poor test score most often indicate?", "Overfitting", "Underfitting", "Perfect generalization", "Balanced classes"),
            ("Which technique can reduce overfitting?", "Regularization", "Adding label leakage", "Training on the test set", "Removing validation"),
        ]),
        ("Features and scaling", [
            ("Why does feature scaling matter for KNN?", "KNN compares distances", "KNN uses only tree depth", "Scaling adds labels", "Scaling converts regression to clustering"),
            ("A feature used by a model should generally be?", "Relevant to the prediction task", "A copy of the target", "Created from test answers", "Constant for every row"),
        ]),
    ],
    "data_analysis_test": [
        ("Missing values", [
            ("Which Pandas call identifies missing cells?", "df.isna()", "df.sort_values()", "df.rename()", "df.tail()"),
            ("Which method removes rows containing missing values?", "dropna()", "fillname()", "remove_nulls()", "dropcols()"),
        ]),
        ("Grouping and aggregation", [
            ("Which Pandas method groups rows by a category?", "groupby()", "pivot_text()", "sort_index()", "reshape_rows()"),
            ("How do you calculate a mean after grouping?", "df.groupby('team')['score'].mean()", "df.mean('team', 'score')", "df.group('team').avg()", "df.aggregate_rows('team')"),
        ]),
        ("Combining data", [
            ("Which Pandas function joins frames using key columns?", "merge()", "describe()", "isna()", "value_counts()"),
            ("Which operation stacks rows from similarly shaped frames?", "concat()", "isnull()", "sort_values()", "astype()"),
        ]),
        ("Exploratory analysis", [
            ("What is the main goal of EDA?", "Understand patterns and relationships in data", "Deploy a web server", "Encrypt every column", "Replace all values with zero"),
            ("Which summary helps inspect numeric spread and quartiles?", "describe()", "rename()", "drop()", "to_csv()"),
        ]),
        ("Charts and distributions", [
            ("Which chart commonly shows a numeric distribution?", "Histogram", "Network diagram", "Flowchart", "Gantt chart"),
            ("Which chart is useful for comparing categories?", "Bar chart", "Histogram only", "Tree map of code", "Sequence diagram"),
        ]),
    ],
    "web_development_test": [
        ("HTML structure", [
            ("Which element represents the main page content?", "<main>", "<meta>", "<style>", "<title>"),
            ("Which element creates a hyperlink?", "<a>", "<linkto>", "<href>", "<url>"),
        ]),
        ("Forms and semantics", [
            ("Which element labels a form control accessibly?", "<label>", "<caption>", "<legendtext>", "<describe>"),
            ("Which input type is intended for email addresses?", "email", "mailbox", "address", "text-email"),
        ]),
        ("CSS layout", [
            ("Which CSS layout system is designed for one-dimensional rows or columns?", "Flexbox", "SQL Grid", "DOM Loop", "HTTP Flow"),
            ("Which property changes text color?", "color", "font-weight", "background-size", "text-align"),
        ]),
        ("JavaScript", [
            ("Which method selects an element by its id?", "document.getElementById()", "window.findId()", "html.selectName()", "document.getClass()"),
            ("Which keyword declares a block-scoped variable that can be reassigned?", "let", "const", "static", "define"),
        ]),
        ("HTTP and accessibility", [
            ("Which HTTP method commonly creates a resource?", "POST", "GET", "HEAD", "TRACE"),
            ("What does alt text provide for an informative image?", "A text description for assistive technology", "A CSS animation", "A database key", "A faster image format"),
        ]),
    ],
    "cybersecurity_test": [
        ("Phishing and social engineering", [
            ("A fake login link sent to steal credentials is?", "Phishing", "Hashing", "Load balancing", "Sandboxing"),
            ("What should you do with an unexpected attachment?", "Verify the sender before opening it", "Enable macros immediately", "Forward it to everyone", "Enter your password to preview it"),
        ]),
        ("Authentication and authorization", [
            ("Authentication verifies a user's?", "Identity", "Permissions only", "Network speed", "File size"),
            ("Authorization determines a user's?", "Allowed actions and resources", "Identity document format", "Password length only", "Internet provider"),
        ]),
        ("Passwords and hashing", [
            ("Why hash stored passwords?", "To store a one-way representation", "To make them readable by staff", "To send them in plain text", "To reuse one password everywhere"),
            ("Which extra value helps defend password hashes against lookup tables?", "A unique salt", "A public username", "A file extension", "A repeated constant"),
        ]),
        ("Web and database security", [
            ("Untrusted input inserted into SQL can cause?", "SQL injection", "DNS caching", "Image compression", "Load shedding"),
            ("What helps prevent SQL injection in application code?", "Parameterized queries", "String concatenation", "Public admin accounts", "Disabling validation"),
        ]),
        ("Network and incident response", [
            ("What does a firewall primarily control?", "Network traffic by defined rules", "Password complexity", "Image metadata", "Database indexes"),
            ("What is a sensible first response to a suspected breach?", "Report and follow the incident response process", "Delete all logs", "Share credentials publicly", "Ignore the alert"),
        ]),
    ],
    "dsa_test": [
        ("Arrays and hashing", [
            ("Which structure provides indexed access by position?", "Array", "Queue", "Tree traversal", "Stack frame"),
            ("Average lookup in a well-designed hash table is typically?", "O(1)", "O(n²)", "O(log n!)", "O(2ⁿ)"),
        ]),
        ("Stacks and queues", [
            ("A stack follows which rule?", "Last in, first out", "First in, first out", "Lowest value first", "Random access only"),
            ("A queue removes which item first?", "The earliest inserted item", "The latest inserted item", "The largest item", "The middle item"),
        ]),
        ("Sorting and searching", [
            ("Binary search requires the input to be?", "Sorted", "Reversed twice", "A linked graph", "All identical"),
            ("What is merge sort's typical time complexity?", "O(n log n)", "O(1)", "O(n²) always", "O(2ⁿ)"),
        ]),
        ("Trees", [
            ("Which BST traversal returns keys in sorted order?", "Inorder", "Preorder", "Postorder", "Random order"),
            ("In a binary tree, a node can have at most how many children?", "Two", "One", "Three", "Unlimited"),
        ]),
        ("Graphs and complexity", [
            ("Which algorithm finds shortest paths with non-negative edge weights?", "Dijkstra's algorithm", "Binary search", "Insertion sort", "BFS on weighted edges without changes"),
            ("Breadth-first search commonly uses which structure?", "Queue", "Stack only", "Heap sort", "Hash function"),
        ]),
    ],
    "aptitude_test": [
        ("Percentages", [
            ("What is 20% of 150?", "30", "20", "15", "45"),
            ("A price rises from 80 to 100. What is the percentage increase?", "25%", "20%", "22%", "80%"),
        ]),
        ("Ratios", [
            ("Simplify the ratio 12:18.", "2:3", "3:2", "6:9", "4:9"),
            ("Divide 40 in the ratio 3:5. What is the smaller share?", "15", "20", "25", "12"),
        ]),
        ("Time and work", [
            ("A completes a task in 6 days. What fraction is done in one day?", "1/6", "1/3", "1/2", "6"),
            ("If 4 workers finish a job in 8 days, worker-days required are?", "32", "12", "4", "8"),
        ]),
        ("Averages", [
            ("What is the mean of 4, 6 and 8?", "6", "5", "7", "18"),
            ("The average of five numbers is 10. Their total is?", "50", "15", "10", "5"),
        ]),
        ("Probability", [
            ("Probability of heads on a fair coin is?", "1/2", "1/4", "1", "0"),
            ("A fair six-sided die is rolled. Probability of an even result?", "1/2", "1/3", "2/3", "1/6"),
        ]),
    ],
    "reasoning_test": [
        ("Number sequences", [
            ("What comes next: 2, 4, 6, 8, ...?", "10", "9", "12", "16"),
            ("What comes next: 3, 6, 12, 24, ...?", "48", "36", "30", "27"),
        ]),
        ("Syllogisms", [
            ("All roses are flowers. A red rose is a rose. What follows?", "The red rose is a flower", "All flowers are roses", "No rose is red", "The red rose is not a flower"),
            ("All A are B. No B are C. Can any A be C?", "No", "Yes, all", "Only one", "Cannot be determined"),
        ]),
        ("Analogies", [
            ("Bird is to nest as bee is to?", "Hive", "Web", "Den", "Stable"),
            ("Book is to reading as fork is to?", "Eating", "Writing", "Listening", "Driving"),
        ]),
        ("Logical deduction", [
            ("A is taller than B, and B is taller than C. Who is shortest?", "C", "A", "B", "Cannot be determined"),
            ("If today is Tuesday, what day is three days later?", "Friday", "Thursday", "Saturday", "Monday"),
        ]),
        ("Patterns and coding", [
            ("If CAT is coded as DBU by shifting each letter one place, DOG becomes?", "EPH", "CNG", "FQI", "DPI"),
            ("Which item does not belong: square, triangle, circle, kilogram?", "Kilogram", "Square", "Triangle", "Circle"),
        ]),
    ],
}


def _build_objective_questions(topic_bank):
    built = {}
    for section_name, topic_specs in topic_bank.items():
        section_questions = []
        for topic_index, (topic_name, pair_specs) in enumerate(topic_specs):
            for question_index, spec in enumerate(pair_specs):
                prompt, correct, distractor_one, distractor_two, distractor_three = spec
                choices = [correct, distractor_one, distractor_two, distractor_three]
                rotate_by = (topic_index + question_index) % len(choices)
                choices = choices[rotate_by:] + choices[:rotate_by]
                section_questions.append({
                    "topic": topic_name,
                    "question": prompt,
                    "options": choices,
                    "answer": correct,
                })
        built[section_name] = section_questions
    return built


OBJECTIVE_ASSESSMENT = _build_objective_questions(OBJECTIVE_TOPIC_BANK)
# ============================================================
# 4. BEHAVIORAL ASSESSMENT
# ============================================================
# Scale:
# 1 = Strongly Disagree
# 2 = Disagree
# 3 = Neutral
# 4 = Agree
# 5 = Strongly Agree
# ============================================================

BEHAVIORAL_SCALE = {
    1: "Strongly Disagree",
    2: "Disagree",
    3: "Neutral",
    4: "Agree",
    5: "Strongly Agree"
}

BEHAVIORAL_QUESTIONS = {

    "communication_skill": [
        "I can explain technical concepts clearly to someone with less technical knowledge.",
        "I can present my ideas in a structured and understandable way.",
        "I listen carefully before responding during discussions.",
        "I can communicate problems clearly when I need help.",
        "I can confidently explain my work during a presentation or interview."
    ],

    "teamwork_skill": [
        "I can work effectively with people who have different ideas from mine.",
        "I contribute my share of work when working on a team project.",
        "I communicate progress and problems with my teammates.",
        "I respect other team members' suggestions even when I disagree.",
        "I can coordinate tasks with teammates to achieve a common goal."
    ],

    "problem_solving_skill": [
        "I break a complex problem into smaller manageable parts.",
        "I try to understand the cause of a problem before changing the solution.",
        "I consider multiple approaches when solving a difficult problem.",
        "I test and verify my solution instead of assuming it is correct.",
        "I can continue working on a problem when the first approach fails."
    ],

    "adaptability_skill": [
        "I can learn a new tool or technology when a project requires it.",
        "I can adjust my approach when requirements change.",
        "I am comfortable learning from mistakes.",
        "I can adapt when working with unfamiliar technologies.",
        "I can continue learning when a topic initially feels difficult."
    ]
}


# ============================================================
# 5. CAREER INTEREST ASSESSMENT
# ============================================================
# Scale:
# 1 = Not Interested
# 2 = Slightly Interested
# 3 = Neutral
# 4 = Interested
# 5 = Highly Interested
# ============================================================

INTEREST_SCALE = {
    1: "Not Interested",
    2: "Slightly Interested",
    3: "Neutral",
    4: "Interested",
    5: "Highly Interested"
}

INTEREST_QUESTIONS = {

    "interest_ai_ml": [
        "I am interested in building machine learning models.",
        "I enjoy learning how AI systems make predictions.",
        "I am interested in working with AI tools and technologies.",
        "I would like to build intelligent applications.",
        "I am interested in solving problems using machine learning.",
    ],

    "interest_data_science": [
        "I enjoy analyzing datasets to find useful patterns.",
        "I am interested in statistics and data-driven decision making.",
        "I would like to create insights from large datasets.",
        "I enjoy creating visualizations and dashboards from data.",
        "I am interested in using data to solve business problems.",
    ],

    "interest_data_analyst": [
        "I enjoy finding trends in business or customer data.",
        "I am interested in using spreadsheets and dashboards to answer questions.",
        "I would like to turn data into practical recommendations for a team.",
        "I enjoy comparing metrics to understand how a business is performing.",
        "I am interested in presenting data insights clearly to decision makers."
    ],

    "interest_software": [
        "I enjoy writing programs to solve practical problems.",
        "I am interested in building software applications.",
        "I enjoy learning programming languages and development tools.",
        "I would like to design and develop software systems.",
        "I am interested in solving programming and algorithmic problems.",
    ],

    "interest_web": [
        "I am interested in building websites and web applications.",
        "I enjoy designing user interfaces.",
        "I am interested in frontend and backend development.",
        "I would like to build interactive web applications.",
        "I enjoy learning web technologies and frameworks.",
    ],

    "interest_cybersecurity": [
        "I am interested in protecting systems and networks from attacks.",
        "I enjoy learning about cybersecurity threats and vulnerabilities.",
        "I am interested in network and application security.",
        "I would like to learn how security incidents are detected and handled.",
        "I am interested in building secure software and systems.",
    ]
}


# ============================================================
# COMPLETE ASSESSMENT STRUCTURE
# ============================================================

ASSESSMENT_QUESTIONS = {
    "basic_info": BASIC_INFO,
    "skill_assessment": SKILL_ASSESSMENT,
    "objective_assessment": OBJECTIVE_ASSESSMENT,
    "behavioral_assessment": BEHAVIORAL_QUESTIONS,
    "interest_assessment": INTEREST_QUESTIONS
}


# ============================================================
# QUICK CHECK
# ============================================================

if __name__ == "__main__":
    print("Assessment question bank loaded successfully.")
    print("Technical skills:", len(SKILL_ASSESSMENT))
    print("Objective sections:", len(OBJECTIVE_ASSESSMENT))

    for section, questions in OBJECTIVE_ASSESSMENT.items():
        print(f"{section}: {len(questions)} questions")

    print("Behavioral sections:", len(BEHAVIORAL_QUESTIONS))
    print("Interest sections:", len(INTEREST_QUESTIONS))
