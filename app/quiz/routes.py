"""
HEADER_COMMENT_AUTOGEN
FILE: app\quiz\routes.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

# app/quiz/routes.py
from flask import render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from . import quiz_bp
from app.models import Category, Question, Attempt, db

@quiz_bp.route('/select')
@login_required
def select():
    categories = Category.query.order_by(Category.name).all()
    return render_template('quiz/select.html', categories=categories)

@quiz_bp.route('/start/<int:category_id>')
@login_required
def start(category_id):
    category = Category.query.get_or_404(category_id)
    return render_template('quiz/select_difficulty.html', category=category)

@quiz_bp.route('/start/<int:category_id>/<difficulty>')
@login_required
def start_quiz(category_id, difficulty):
    category = Category.query.get_or_404(category_id)
    # Filter questions by category and difficulty
    questions = Question.query.filter_by(
        category_id=category_id,
        difficulty=difficulty
    ).all()
    
    if not questions:
        flash(f'No {difficulty} questions available in this category', 'warning')
        return redirect(url_for('quiz.start', category_id=category_id))
    
    # Limit to 10 questions
    questions = questions[:10]
    
    # Initialize quiz session (convert IDs to strings for JSON serialization)
    session['quiz_category_id'] = str(category_id)
    session['quiz_difficulty'] = difficulty
    session['quiz_questions'] = [str(q.id) for q in questions]
    session['current_question_index'] = 0
    session['quiz_score'] = 0
    session['quiz_answers'] = {}
    return redirect(url_for('quiz.question', q_id=questions[0].id))

@quiz_bp.route('/question/<int:q_id>', methods=['GET', 'POST'])
@login_required
def question(q_id):
    if 'quiz_questions' not in session:
        flash('Please select a category first', 'warning')
        return redirect(url_for('quiz.select'))
    
    q = Question.query.get_or_404(q_id)
    # Convert q_id to string for session comparison
    q_id_str = str(q_id)
    if q_id_str not in session['quiz_questions']:
        flash('Invalid question', 'danger')
        return redirect(url_for('quiz.select'))
    
    if request.method == 'POST':
        chosen_option = int(request.form.get('option', 0))
        # Store answer with string key
        session['quiz_answers'][q_id_str] = chosen_option
        
        # Check if correct
        if chosen_option == q.correct_option:
            session['quiz_score'] = session.get('quiz_score', 0) + 1
        
        # Move to next question
        current_idx = session['current_question_index'] + 1
        session['current_question_index'] = current_idx
        
        if current_idx < len(session['quiz_questions']):
            next_q_id = int(session['quiz_questions'][current_idx])  # Convert back to int for URL
            return redirect(url_for('quiz.question', q_id=next_q_id))
        else:
            # Quiz completed
            return redirect(url_for('quiz.result'))
    
    # GET request - show question
    return render_template('quiz/question.html', question=q, 
                         question_num=session['current_question_index'] + 1,
                         total=len(session['quiz_questions']))

@quiz_bp.route('/result')
@login_required
def result():
    if 'quiz_score' not in session:
        flash('No quiz session found', 'warning')
        return redirect(url_for('quiz.select'))
    
    score = session.get('quiz_score', 0)
    total = len(session.get('quiz_questions', []))
    category_id = session.get('quiz_category_id')
    
    # Save attempt to database
    if category_id:
        # Convert category_id back to int if it's a string
        cat_id = int(category_id) if isinstance(category_id, str) else category_id
        difficulty = session.get('quiz_difficulty', None)
        attempt = Attempt(
            user_id=current_user.id,
            score=score,
            total=total,
            category_id=cat_id,
            difficulty=difficulty
        )
        db.session.add(attempt)
        db.session.commit()
    
    # Clear quiz session
    session.pop('quiz_category_id', None)
    session.pop('quiz_difficulty', None)
    session.pop('quiz_questions', None)
    session.pop('current_question_index', None)
    session.pop('quiz_answers', None)
    quiz_score = session.pop('quiz_score', 0)
    
    return render_template('quiz/result.html', score=quiz_score, total=total)
