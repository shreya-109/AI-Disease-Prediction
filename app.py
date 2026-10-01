from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
import joblib
import pandas as pd

from database import (
    create_table,
    save_prediction,
    get_predictions,
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_dashboard_stats,
    verify_password
)


# Create Flask application
app = Flask(__name__)

app.secret_key = "ai-disease-prediction-secret-key"

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

#user loader callback for Flask-Login
class User(UserMixin):

    def __init__(self, user_id, username, email):

        self.id = user_id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):

    connection = sqlite3.connect("predictions.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, username, email FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    connection.close()

    if user:

        return User(
            user["id"],
            user["username"],
            user["email"]
        )

    return None


# Create database table when application starts
create_table()


# Load trained ML model
model = joblib.load("model/disease_model.pkl")


# Symptoms used by our ML model
SYMPTOMS = [
    "fever",
    "cough",
    "fatigue",
    "headache",
    "sore_throat",
    "nausea",
    "vomiting",
    "joint_pain",
    "skin_rash",
    "stomach_pain"
]


# ---------------- HOME PAGE ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- PREDICTION API ----------------

@app.route("/predict", methods=["POST"])
@login_required
def predict():

    # Get JSON data from frontend
    data = request.get_json()

    # Get selected symptoms
    selected_symptoms = data.get("symptoms", [])

    # Validate symptoms
    if not selected_symptoms:
        return jsonify({
            "error": "Please select at least one symptom."
        }), 400

    # Create input dictionary
    input_data = {}

    for symptom in SYMPTOMS:

        if symptom in selected_symptoms:
            input_data[symptom] = 1
        else:
            input_data[symptom] = 0

    # Convert input into DataFrame
    input_df = pd.DataFrame([input_data])

    # Predict disease
    prediction = model.predict(input_df)[0]

    # Get probability for each disease
    probabilities = model.predict_proba(input_df)[0]

    # Calculate highest probability
    confidence = max(probabilities) * 100

    # Round confidence
    confidence = round(confidence, 2)
    # Save prediction into database
    save_prediction(
        current_user.id,
        selected_symptoms,
        prediction,
        confidence
    )

    # Send result back to frontend
    return jsonify({
        "disease": prediction,
        "confidence": confidence,
        "symptoms": selected_symptoms
    })    # Save prediction into database

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
@login_required
def dashboard():

    stats = get_dashboard_stats(current_user.id)

    predictions = get_predictions(current_user.id)

    return render_template(
        "dashboard.html",
        stats=stats,
        predictions=predictions[:5]
    )

# ---------------- PREDICTION HISTORY ----------------

@app.route("/history")
@login_required
def history():

    # Get all saved predictions
    predictions = get_predictions(current_user.id)

    # Send predictions to history page
    return render_template(
        "history.html",
        predictions=predictions
    )

#---------------- EVALUATION METRICS ----------------
@app.route("/evaluation")
def evaluation():

    metrics = {}

    with open("model/evaluation.txt", "r") as file:

        for line in file:

            key, value = line.strip().split(":")

            metrics[key] = value

    return render_template(
        "evaluation.html",
        metrics=metrics
    )

#---------------- USER REGISTRATION ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        user_id = create_user(
            username,
            email,
            password
        )

        if user_id is None:

            return "Email already registered."

        return redirect(url_for("login"))

    return render_template("register.html")

# ---------------- USER LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = get_user_by_email(email)

        if user is None:
            return "Invalid email or password."

        if not verify_password(password, user["password"]):
            return "Invalid email or password."

        # Create Flask-Login user object
        user_obj = User(
            user["id"],
            user["username"],
            user["email"]
        )

        # Log the user in
        login_user(user_obj)

        return redirect(url_for("home"))

    return render_template("login.html")


# ---------------- USER LOGOUT ----------------

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))
# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":

    app.run(
        debug=True
    )


