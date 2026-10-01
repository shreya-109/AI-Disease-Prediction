import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "predictions.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")

    # -----------------------------------------------------
    # USERS TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # -----------------------------------------------------
    # PREDICTIONS TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symptoms TEXT NOT NULL,
            disease TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()


# =========================================================
# CREATE NEW USER
# =========================================================

def create_user(username, email, password):

    connection = get_connection()
    cursor = connection.cursor()

    hashed_password = generate_password_hash(password)

    try:

        cursor.execute("""
            INSERT INTO users
            (username, email, password)
            VALUES (?, ?, ?)
        """, (
            username,
            email,
            hashed_password
        ))

        connection.commit()

        user_id = cursor.lastrowid

        connection.close()

        return user_id

    except sqlite3.IntegrityError:

        connection.close()

        return None


# =========================================================
# GET USER BY EMAIL
# =========================================================

def get_user_by_email(email):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            email,
            password,
            created_at
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    connection.close()

    return user


# =========================================================
# GET USER BY ID
# =========================================================

def get_user_by_id(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            email,
            created_at
        FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()

    connection.close()

    return user


# =========================================================
# VERIFY PASSWORD
# =========================================================

def verify_password(password, hashed_password):

    return check_password_hash(
        hashed_password,
        password
    )


# =========================================================
# SAVE PREDICTION
# =========================================================

def save_prediction(user_id, symptoms, disease, confidence):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO predictions
        (
            user_id,
            symptoms,
            disease,
            confidence
        )
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        ", ".join(symptoms),
        disease,
        confidence
    ))

    connection.commit()

    prediction_id = cursor.lastrowid

    connection.close()

    return prediction_id


# =========================================================
# GET USER'S PREDICTIONS
# =========================================================

def get_predictions(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            symptoms,
            disease,
            confidence,
            created_at
        FROM predictions
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))

    predictions = cursor.fetchall()

    connection.close()

    return predictions


# =========================================================
# GET PREDICTION COUNT
# =========================================================

def get_prediction_count(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE user_id = ?
    """, (user_id,))

    count = cursor.fetchone()[0]

    connection.close()

    return count


# =========================================================
# GET ALL USERS
# =========================================================

def get_all_users():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            email,
            created_at
        FROM users
        ORDER BY created_at DESC
    """)

    users = cursor.fetchall()

    connection.close()

    return users
# =========================================================
# GET DASHBOARD STATISTICS
# =========================================================

def get_dashboard_stats(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    # Total predictions
    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE user_id = ?
    """, (user_id,))

    total_predictions = cursor.fetchone()[0]

    # Average confidence
    cursor.execute("""
        SELECT AVG(confidence)
        FROM predictions
        WHERE user_id = ?
    """, (user_id,))

    average_confidence = cursor.fetchone()[0]

    if average_confidence is None:
        average_confidence = 0

    # Most predicted disease
    cursor.execute("""
        SELECT disease, COUNT(*) AS count
        FROM predictions
        WHERE user_id = ?
        GROUP BY disease
        ORDER BY count DESC
        LIMIT 1
    """, (user_id,))

    most_predicted = cursor.fetchone()

    if most_predicted:
        most_predicted_disease = most_predicted["disease"]
    else:
        most_predicted_disease = "No predictions yet"

    connection.close()

    return {
        "total_predictions": total_predictions,
        "average_confidence": round(average_confidence, 2),
        "most_predicted_disease": most_predicted_disease
    }