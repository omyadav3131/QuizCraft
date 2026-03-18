# QuizCraft – Online Quiz & Competition Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-green)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-orange)
![Bootstrap](https://img.shields.io/badge/UI-Bootstrap-purple)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)

QuizCraft is a full-stack web application built using the **Flask framework** that allows users to take quizzes based on category and difficulty level, track their performance, and compete with other users through multiplayer quiz competitions.

The platform includes automated scoring, leaderboards, performance analytics, and a role-based admin panel for managing questions, categories, and users.

---

## Project Overview

QuizCraft provides an interactive environment for knowledge testing and learning.
Users can participate in quizzes, view their progress through analytics dashboards, and compete in multiplayer competitions.

Administrators can manage quiz content through a dedicated admin interface.

Core capabilities include:

* Category-based quiz system
* Difficulty level selection
* Automated score calculation
* Performance tracking
* Multiplayer quiz competitions
* Leaderboard ranking system
* Admin management dashboard

---

## Key Features

### User Features

* User registration and login authentication
* Category and difficulty-based quiz selection
* Timed quizzes with automated scoring
* Detailed result analysis with correct answers
* Performance dashboard showing statistics and trends
* Leaderboard displaying top users

### Competition Mode

* Two-player quiz competitions
* Create or join competitions using a unique code
* Simultaneous quiz attempts for both players
* Automatic winner calculation after completion

### Admin Panel

* Manage quiz categories
* Add, edit, and delete questions
* Bulk question upload functionality
* Manage users and roles
* Monitor leaderboard and feedback data

---

## Tech Stack

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-WTF
* Flask-Migrate

### Database

* SQLite (development)
* PostgreSQL (production compatible)

### Frontend

* HTML
* CSS
* Bootstrap
* Jinja2 Templates

### Tools

* Git
* GitHub
* Docker (optional deployment support)

---

## System Architecture

```
User (Browser)
      |
      v
Frontend (HTML, CSS, Bootstrap)
      |
      v
Flask Application (Routes & Controllers)
      |
      v
Quiz Logic & Competition Engine
      |
      v
SQLAlchemy ORM
      |
      v
Database (SQLite / PostgreSQL)
```

---

## Project Structure

```
QuizCraft
│
├── app
│   ├── auth              # Authentication system
│   ├── admin             # Admin dashboard
│   ├── quiz              # Quiz functionality
│   ├── competition       # Multiplayer quiz competitions
│   ├── models.py         # Database models
│   └── routes.py         # Application routes
│
├── migrations            # Database migrations
├── static                # CSS, JS, images
├── templates             # HTML templates
│
├── config.py             # Configuration settings
├── create_db.py          # Database initialization
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
│
├── README.md
└── LICENSE
```

---

## Installation

### Clone the repository

```
git clone https://github.com/omyadav3131/QuizCraft.git
cd QuizCraft
```

### Create virtual environment

Windows:

```
python -m venv venv
venv\Scripts\activate
```

Linux / Mac:

```
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```
pip install -r requirements.txt
```

### Initialize the database

```
python create_db.py
```

### Run the application

```
python main.py
```

Open the application in your browser:

```
http://127.0.0.1:5000
```

---

## Database Models

The application uses relational models to manage quiz and competition data.

Main entities include:

* **User** – stores user accounts and roles
* **Category** – quiz categories
* **Question** – questions with multiple options and correct answer
* **Attempt** – records quiz attempts
* **AttemptAnswer** – stores answers selected by users
* **Competition** – multiplayer quiz competitions
* **CompetitionAttempt** – attempts made within competitions
* **LeaderboardEntry** – ranking data for users
* **Feedback** – user feedback and ratings

---

## Security Features

* Password hashing using Werkzeug
* CSRF protection using Flask-WTF
* Session management with Flask-Login
* Role-based access control for admin features

---

## Future Improvements

Potential improvements for the platform:

* Real-time competitions using WebSockets
* Advanced analytics dashboards
* REST API support for mobile applications
* Cloud deployment and scalability improvements

---

## Author

Om Yadav

GitHub
https://github.com/omyadav3131

---

## License

This project is licensed under the MIT License.
