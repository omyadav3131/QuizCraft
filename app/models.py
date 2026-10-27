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
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(20), default=Role.USER)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    verified_at = db.Column(db.DateTime, nullable=True)
    google_id = db.Column(db.String(255), unique=True, nullable=True)
    attempts = db.relationship('Attempt', backref='user', lazy=True)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)
    def check_password(self, pw):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, pw)
    def is_admin(self):
        return self.role == Role.ADMIN

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

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


# ══════════════════════════════════════════════════════════════════
# Placement Mock Test Models (TCS NQT Style & Anti-Cheat Engine)
# ══════════════════════════════════════════════════════════════════

class MockTest(db.Model):
    """Placement mock test model (e.g. TCS NQT, Infosys, Wipro)."""
    __tablename__ = 'mock_test'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration_minutes = db.Column(db.Integer, default=60, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    allow_multiple_attempts = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    sections = db.relationship(
        'MockSection',
        backref='test',
        lazy=True,
        cascade='all, delete-orphan',
        order_by='MockSection.order'
    )
    attempts = db.relationship(
        'MockAttempt',
        backref='test',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def total_questions_count(self):
        return sum(len(s.questions) for s in self.sections)

    def total_marks(self):
        return sum(sum(q.marks for q in s.questions) for s in self.sections)


class MockSection(db.Model):
    """Section of a mock test (e.g. Numerical Ability, Verbal Ability, Reasoning Ability)."""
    __tablename__ = 'mock_section'

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('mock_test.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    order = db.Column(db.Integer, default=1, nullable=False)
    num_questions = db.Column(db.Integer, default=10, nullable=False)
    section_minutes = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    questions = db.relationship(
        'MockQuestion',
        backref='section',
        lazy=True,
        cascade='all, delete-orphan',
        order_by='MockQuestion.id'
    )


class MockQuestion(db.Model):
    """Question belonging to a specific mock section."""
    __tablename__ = 'mock_question'

    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('mock_section.id'), nullable=False, index=True)
    text = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.Text, nullable=True)
    option2 = db.Column(db.Text, nullable=True)
    option3 = db.Column(db.Text, nullable=True)
    option4 = db.Column(db.Text, nullable=True)
    correct_option = db.Column(db.Integer, nullable=False)  # 1..4
    explanation = db.Column(db.Text, nullable=True)
    marks = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class MockAttempt(db.Model):
    """Single student attempt on a mock test with server-side deadline & tracking."""
    __tablename__ = 'mock_attempt'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    test_id = db.Column(db.Integer, db.ForeignKey('mock_test.id'), nullable=False, index=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    server_deadline = db.Column(db.DateTime, nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(30), default='in_progress', nullable=False)  # 'in_progress', 'completed', 'timed_out', 'disqualified'
    score = db.Column(db.Integer, default=0, nullable=False)
    total_marks = db.Column(db.Integer, default=0, nullable=False)
    violation_count = db.Column(db.Integer, default=0, nullable=False)
    question_order = db.Column(db.JSON, nullable=True)  # Stores student's randomized question sequence & option mapping

    # Relationships
    user = db.relationship('User', backref=db.backref('mock_attempts', lazy=True))
    answers = db.relationship(
        'MockAnswer',
        backref='attempt',
        lazy=True,
        cascade='all, delete-orphan'
    )


class MockAnswer(db.Model):
    """Student's answer to a single question in a mock attempt."""
    __tablename__ = 'mock_answer'

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('mock_attempt.id'), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey('mock_question.id'), nullable=False, index=True)
    chosen_option = db.Column(db.Integer, nullable=True)  # 1..4 in canonical question order, or None
    marked_for_review = db.Column(db.Boolean, default=False, nullable=False)
    time_spent = db.Column(db.Integer, default=0, nullable=False)  # seconds
    is_correct = db.Column(db.Boolean, nullable=True)

    # Relationships
    question = db.relationship('MockQuestion', lazy=True)


class MockViolation(db.Model):
    """Anti-cheat discipline logs for student mock attempts."""
    __tablename__ = 'mock_violation'

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('mock_attempt.id'), nullable=False, index=True)
    violation_type = db.Column(db.String(50), nullable=False)  # 'tab_switch', 'window_blur', 'fullscreen_exit'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    attempt = db.relationship(
        'MockAttempt',
        backref=db.backref('violations', lazy=True, cascade='all, delete-orphan', order_by='MockViolation.timestamp')
    )

