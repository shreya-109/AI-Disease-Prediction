# 🩺 AI Disease Prediction System

An AI-powered web application that predicts a possible disease based on selected symptoms using a trained Machine Learning model.

The application provides a simple interface where users can select symptoms, receive an ML-based prediction with confidence, and securely maintain their personal prediction history.

> **Note:** This project is developed for educational purposes and is not a replacement for professional medical diagnosis.

---

## 🚀 Features

* 🧠 Machine Learning-based disease prediction
* 🩺 Select multiple symptoms
* 📊 Prediction confidence percentage
* 👤 User registration and login
* 🔐 Password hashing and authentication
* 📋 User-specific prediction history
* 📈 Model evaluation metrics
* 📊 Personalized dashboard
* 🔒 User prediction data separated by account
* 🗃️ SQLite database integration
* 🌐 Flask-based web application
* 📱 Responsive and user-friendly interface

---

## 🛠️ Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask
* Flask-Login

### Machine Learning

* Scikit-learn
* Pandas
* Joblib

### Database

* SQLite

### Security

* Werkzeug Password Hashing
* Flask-Login Authentication

---

## 🏗️ Project Structure

```text
AI-Disease-Prediction/
│
├── app.py
├── database.py
├── train_model.py
├── requirements.txt
├── README.md
│
├── data/
│   └── dataset files
│
├── model/
│   ├── disease_model.pkl
│   └── evaluation.txt
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── history.html
    └── evaluation.html
```

---

## ⚙️ How It Works

```text
User
  ↓
Select Symptoms
  ↓
Flask Backend
  ↓
Prepare Symptom Data
  ↓
Machine Learning Model
  ↓
Disease Prediction
  ↓
Confidence Score
  ↓
Save Result in Database
  ↓
Display Result & History
```

---

## 🧠 Machine Learning Workflow

The system uses symptom information as input to a trained Machine Learning model.

The selected symptoms are converted into numerical values:

```text
Selected symptom     → 1
Unselected symptom   → 0
```

The resulting data is passed to the trained model.

The model generates:

* Predicted disease
* Prediction probability
* Confidence percentage

---

## 🩺 Supported Symptoms

The current version supports:

* Fever
* Cough
* Fatigue
* Headache
* Sore Throat
* Nausea
* Vomiting
* Joint Pain
* Skin Rash
* Stomach Pain

---

## 👤 User Authentication

The application provides:

### Registration

Users can create an account using:

* Username
* Email
* Password

Passwords are stored using secure password hashing rather than plain text.

### Login

Registered users can log in using their email and password.

### Logout

Users can securely log out of their account.

### Prediction History

Each prediction is associated with the logged-in user's account.

---

## 📊 Dashboard

The dashboard provides an overview of the user's prediction activity.

It displays:

* Total predictions
* Average confidence
* Most predicted disease
* Recent activity
* Recent prediction history

---

## 📈 Model Evaluation

The application includes an evaluation page for displaying model performance metrics generated during model evaluation.

Example metrics may include:

* Accuracy
* Precision
* Recall
* F
