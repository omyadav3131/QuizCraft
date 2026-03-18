QuizCraft – Flask Quiz & Competition Platform








QuizCraft is a feature-rich quiz platform built using the Flask web framework.
The application allows users to take quizzes based on category and difficulty level, track their performance, and participate in competitions with other users. It also includes an admin panel for managing questions, categories, and users.

Key Features
User Features

User registration and authentication system

Category and difficulty-based quiz selection

Automated quiz evaluation and scoring

Performance dashboard with statistics

Leaderboard ranking system

Detailed result analysis with explanations

Feedback submission system

Competition Mode

Two-player quiz competition

Create or join competitions using a unique code

Simultaneous quiz attempts for both players

Automatic winner calculation

Admin Panel

Manage quiz categories

Add, edit, or delete questions

Bulk question upload

Manage users and roles

View feedback and leaderboard statistics

Tech Stack

Backend

Python

Flask

Flask-SQLAlchemy

Flask-Migrate

Flask-WTF

Flask-Login

Database

SQLite (development)

PostgreSQL (production)

Frontend

HTML

CSS

Bootstrap

Font Awesome

Tools

Git

GitHub

Project Structure
quizcraft/
│
├── app/
│   ├── auth/           # Authentication routes
│   ├── admin/          # Admin dashboard
│   ├── quiz/           # Quiz system routes
│   ├── competition/    # Competition mode
│   ├── static/         # CSS, images
│   └── templates/      # HTML templates
│
├── migrations/         # Database migration files
├── config.py           # Application configuration
├── create_db.py        # Database initialization
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
└── README.md
Installation
Prerequisites

Python 3.8 or higher

pip

Git

Clone the Repository
git clone https://github.com/omyadav3131/QuizCraft.git
cd QuizCraft
Create Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate

Linux / Mac

python3 -m venv venv
source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Initialize Database
python create_db.py
flask db upgrade
Run the Application
python main.py

Open the application in your browser:

http://127.0.0.1:5000
Core Database Models

The application uses relational database models to manage quiz data.

Main entities include:

User – Stores user accounts and roles

Category – Quiz categories

Question – Quiz questions with difficulty levels

Attempt – Records quiz attempts

AttemptAnswer – Stores answers for each question

Competition – Two-player quiz competitions

LeaderboardEntry – Stores ranking information

Feedback – Stores user feedback and ratings

Security Features

Password hashing using Werkzeug

CSRF protection with Flask-WTF

Session management with Flask-Login

Role-based access control for admin features

Future Improvements

Real-time competition using WebSockets

Advanced analytics dashboards

REST API for mobile applications

Cloud deployment and scalability improvements

License

This project is licensed under the MIT License.

Author

Om Yadav

GitHub Repository:
https://github.com/omyadav3131/QuizCraft

⭐ If you find this project useful, consider giving it a star.
