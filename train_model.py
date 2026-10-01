
import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# -----------------------------------
# Load dataset
# -----------------------------------

data = pd.read_csv("data/disease_data.csv")


# -----------------------------------
# Input features
# -----------------------------------

X = data.drop("disease", axis=1)


# -----------------------------------
# Target variable
# -----------------------------------

y = data["disease"]


# -----------------------------------
# Split dataset
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.35,
    random_state=42,
    stratify=y
)


# -----------------------------------
# Create Random Forest model
# -----------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# -----------------------------------
# Train model
# -----------------------------------

model.fit(X_train, y_train)


# -----------------------------------
# Make predictions
# -----------------------------------

y_pred = model.predict(X_test)


# -----------------------------------
# Model Evaluation
# -----------------------------------

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)


# -----------------------------------
# Display results
# -----------------------------------

print("\n====================================")
print("       MODEL EVALUATION")
print("====================================")

print("Accuracy :", round(accuracy * 100, 2), "%")
print("Precision:", round(precision * 100, 2), "%")
print("Recall   :", round(recall * 100, 2), "%")
print("F1 Score :", round(f1 * 100, 2), "%")

# Save evaluation metrics
with open("model/evaluation.txt", "w") as file:

    file.write(f"Accuracy: {accuracy * 100:.2f}%\n")
    file.write(f"Precision: {precision * 100:.2f}%\n")
    file.write(f"Recall: {recall * 100:.2f}%\n")
    file.write(f"F1 Score: {f1 * 100:.2f}%\n")
# -----------------------------------
# Classification Report
# -----------------------------------

print("\n====================================")
print("       CLASSIFICATION REPORT")
print("====================================")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# -----------------------------------
# Confusion Matrix
# -----------------------------------

print("\n====================================")
print("       CONFUSION MATRIX")
print("====================================")

print(confusion_matrix(y_test, y_pred))


# -----------------------------------
# Create model directory
# -----------------------------------

os.makedirs("model", exist_ok=True)


# -----------------------------------
# Save trained model
# -----------------------------------

joblib.dump(
    model,
    "model/disease_model.pkl"
)


print("\n====================================")
print("Model trained successfully!")
print("Model saved successfully!")
print("====================================")
