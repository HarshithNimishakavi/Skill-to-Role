import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# Load dataset
a = pd.read_csv("data/student_dataset.csv")

# Remove unwanted columns
a = a.drop(columns=["student_id"])


# Separate input and output
x = a.iloc[:, :-1]
y = a["career_role"]

print("INPUT FEATURES SHAPE")
print(x.shape)


# Train-Test Split
x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Tuned Random Forest
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    min_samples_split=2,
    random_state=42
)


# Train model
rf.fit(x_train, y_train)


# Get feature importance
importance = rf.feature_importances_


# Create feature importance table
feature_importance = pd.DataFrame({
    "Feature": x.columns,
    "Importance": importance
})


# Sort from highest to lowest
feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)


print("\nFEATURE IMPORTANCE")
print(feature_importance.to_string(index=False))