"""
HEADER_COMMENT_AUTOGEN
FILE: app\models.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

# app/models.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager

class Role:
    USER = 'user'
    ADMIN = 'admin'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default=Role.USER)
    attempts = db.relationship('Attempt', backref='user', lazy=True)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)
    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)
    def is_admin(self):
        return self.role == Role.ADMIN

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    questions = db.relationship('Question', backref='category', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255), nullable=True)
    option2 = db.Column(db.String(255), nullable=True)
    option3 = db.Column(db.String(255), nullable=True)
    option4 = db.Column(db.String(255), nullable=True)
    correct_option = db.Column(db.Integer, nullable=False)  # 1..4
    explanation = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    difficulty = db.Column(db.String(20), nullable=True)   # 'Easy','Medium','Hard'

class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer)
    total = db.Column(db.Integer)
    points = db.Column(db.Integer, default=0)  # Points based on difficulty (Easy=2, Medium=4, Hard=6)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    difficulty = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    answers = db.relationship('AttemptAnswer', backref='attempt', lazy=True)

class AttemptAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempt.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    chosen_option = db.Column(db.Integer)  # 1..4
    correct = db.Column(db.Boolean)
    # backref to question via relationship not necessary but convenient:
    question = db.relationship('Question', primaryjoin='Question.id==AttemptAnswer.question_id', uselist=False)

class LeaderboardEntry(db.Model):
    __tablename__ = 'leaderboard'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    username = db.Column(db.String(150), nullable=False)

    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=True)
    points = db.Column(db.Integer, default=0)  # Points based on difficulty

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    difficulty = db.Column(db.String(20), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref='leaderboard_entries', lazy=True)
    category = db.relationship('Category', lazy=True)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    feedback_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='feedbacks', lazy=True)


class Competition(db.Model):
    """Multiplayer competition between 2 users"""
    __tablename__ = 'competition'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), unique=True, nullable=False, index=True)  # Unique join code
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # Easy, Medium, Hard
    num_questions = db.Column(db.Integer, default=10)
    time_limit = db.Column(db.Integer, default=600)  # seconds
    status = db.Column(db.String(20), default='waiting')  # waiting, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime, nullable=True)
    ended_at = db.Column(db.DateTime, nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Relationships
    creator = db.relationship('User', foreign_keys=[creator_id], backref='competitions_created')
    category = db.relationship('Category', backref='competitions')
    winner = db.relationship('User', foreign_keys=[winner_id])
    attempts = db.relationship('CompetitionAttempt', cascade='all, delete-orphan', lazy=True)


class CompetitionAttempt(db.Model):
    """Individual attempt in a competition"""
    __tablename__ = 'competition_attempt'
    
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Float, default=0.0)  # percentage
    correct_answers = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer)
    time_taken = db.Column(db.Integer, nullable=True)  # seconds
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    answers = db.Column(db.JSON, default={})  # {question_id: selected_option}
    
    # Relationships
    user = db.relationship('User', backref='competition_attempts', lazy=True)
    competition = db.relationship('Competition', backref='user_attempts', lazy=True)
