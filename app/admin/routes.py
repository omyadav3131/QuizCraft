"""
HEADER_COMMENT_AUTOGEN
FILE: app\admin\routes.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

# app/admin/routes.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.admin import admin_bp
from app.models import db, Question, Category, User, Competition, CompetitionAttempt
from datetime import datetime, timedelta

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Admin access required', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper

@admin_bp.route('/competitions')
@login_required
@admin_required
def competitions_view():
    """Admin view of all multiplayer competitions"""
    # Get date filter from query params
    date_filter = request.args.get('date_filter', default='all', type=str)  # today, week, month, all
    
    # Calculate date range based on filter
    today = datetime.utcnow().date()
    if date_filter == 'today':
        from_date = datetime.combine(today, datetime.min.time())
        to_date = datetime.combine(today, datetime.max.time())
    elif date_filter == 'week':
        from_date = datetime.utcnow() - timedelta(days=7)
        to_date = datetime.utcnow()
    elif date_filter == 'month':
        from_date = datetime.utcnow() - timedelta(days=30)
        to_date = datetime.utcnow()
    else:  # all
        from_date = datetime.min
        to_date = datetime.utcnow()
    
    # Get competitions within date range, ordered by creation date (newest first)
    competitions = Competition.query.filter(
        Competition.created_at >= from_date,
        Competition.created_at <= to_date
    ).order_by(Competition.created_at.desc()).all()
    
    # Prepare detailed competition data
    comp_data = []
    for comp in competitions:
        # Get creator and participants
        creator = User.query.get(comp.creator_id)
        attempts = CompetitionAttempt.query.filter_by(competition_id=comp.id).all()
        participants = [User.query.get(att.user_id) for att in attempts]
        
        # Calculate winner
        winner_name = User.query.get(comp.winner_id).username if comp.winner_id else 'N/A'
        
        # Get scores
        scores = [(User.query.get(att.user_id).username, att.correct_answers, att.total_questions) for att in attempts]
        
        comp_data.append({
            'id': comp.id,
            'code': comp.code,
            'category': comp.category.name if comp.category else 'N/A',
            'difficulty': comp.difficulty,
            'creator': creator.username if creator else 'N/A',
            'participants': ', '.join([p.username for p in participants if p]),
            'status': comp.status,
            'scores': scores,
            'winner': winner_name,
            'created_at': comp.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'started_at': comp.started_at.strftime('%Y-%m-%d %H:%M:%S') if comp.started_at else 'N/A',
            'ended_at': comp.ended_at.strftime('%Y-%m-%d %H:%M:%S') if comp.ended_at else 'N/A'
        })
    
    return render_template('admin/competitions.html', competitions=comp_data, date_filter=date_filter)

@admin_bp.route('/')
@login_required
@admin_required
def index():
    # Get all categories and their questions
    categories = Category.query.order_by(Category.name).all()
    category_questions = {}
    total_questions = 0
    
    for cat in categories:
        questions = Question.query.filter_by(category_id=cat.id).order_by(
            Question.difficulty.desc(), 
            Question.id.desc()
        ).all()
        category_questions[cat.id] = questions
        total_questions += len(questions)
    
    return render_template('admin/index.html', 
                         categories=categories,
                         category_questions=category_questions,
                         total_questions=total_questions)

@admin_bp.route('/categories', methods=['GET','POST'])
@login_required
@admin_required
def categories():
    if request.method == 'POST':
        name = request.form.get('name').strip()
        if name:
            if Category.query.filter_by(name=name).first():
                flash('Category already exists', 'warning')
            else:
                db.session.add(Category(name=name))
                db.session.commit()
                flash('Category added', 'success')
        return redirect(url_for('admin.categories'))
    cats = Category.query.order_by(Category.name).all()
    return render_template('admin/categories.html', categories=cats)

@admin_bp.route('/question/new', methods=['GET','POST'])
@login_required
@admin_required
def new_question():
    cats = Category.query.order_by(Category.name).all()
    if request.method == 'POST':
        q = Question(
            text=request.form['text'],
            option1=request.form['option1'],
            option2=request.form['option2'],
            option3=request.form.get('option3'),
            option4=request.form.get('option4'),
            correct_option=int(request.form['correct_option']),
            explanation=request.form.get('explanation',''),
            category_id=int(request.form['category']) if request.form.get('category') else None,
            difficulty=request.form.get('difficulty')
        )
        db.session.add(q); db.session.commit()
        flash('Question added', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/question_form.html', categories=cats, question=None)

@admin_bp.route('/question/edit/<int:q_id>', methods=['GET','POST'])
@login_required
@admin_required
def edit_question(q_id):
    q = Question.query.get_or_404(q_id)
    cats = Category.query.order_by(Category.name).all()
    if request.method == 'POST':
        q.text = request.form['text']
        q.option1 = request.form['option1']
        q.option2 = request.form['option2']
        q.option3 = request.form.get('option3')
        q.option4 = request.form.get('option4')
        q.correct_option = int(request.form['correct_option'])
        q.explanation = request.form.get('explanation','')
        q.category_id = int(request.form['category']) if request.form.get('category') else None
        q.difficulty = request.form.get('difficulty')
        db.session.commit()
        flash('Question updated', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/question_form.html', categories=cats, question=q)

@admin_bp.route('/question/delete/<int:q_id>', methods=['POST'])
@login_required
@admin_required
def delete_question(q_id):
    q = Question.query.get_or_404(q_id)
    db.session.delete(q); db.session.commit()
    flash('Question deleted', 'success')
    return redirect(url_for('admin.index'))

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.order_by(User.id.desc()).all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/user/new', methods=['GET','POST'])
@login_required
@admin_required
def new_user():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        email = request.form.get('email','').strip() or None
        password = request.form.get('password','').strip()
        role = request.form.get('role', 'user')

        if not username or not password:
            flash('Username and password are required', 'warning')
            return redirect(url_for('admin.new_user'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'warning')
            return redirect(url_for('admin.new_user'))

        u = User(username=username, email=email, role=role)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        flash('User created successfully', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user_form.html', user=None)


@admin_bp.route('/user/edit/<int:user_id>', methods=['GET','POST'])
@login_required
@admin_required
def edit_user(user_id):
    u = User.query.get_or_404(user_id)
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        email = request.form.get('email','').strip() or None
        password = request.form.get('password','').strip()
        role = request.form.get('role', 'user')

        if username:
            # check uniqueness
            other = User.query.filter_by(username=username).first()
            if other and other.id != u.id:
                flash('Username already taken', 'warning')
                return redirect(url_for('admin.edit_user', user_id=u.id))
            u.username = username

        u.email = email
        u.role = role
        if password:
            u.set_password(password)

        db.session.commit()
        flash('User updated', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user_form.html', user=u)


@admin_bp.route('/user/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    u = User.query.get_or_404(user_id)
    # Prevent deleting own account
    if u.id == current_user.id:
        flash('You cannot delete your own account', 'warning')
        return redirect(url_for('admin.users'))

    db.session.delete(u)
    db.session.commit()
    flash('User deleted', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/questions/bulk-add', methods=['GET','POST'])
@login_required
@admin_required
def bulk_add_questions():
    cats = Category.query.order_by(Category.name).all()
    if request.method == 'POST':
        # Get number of questions to add
        num_questions = int(request.form.get('num_questions', 1))
        added_count = 0
        errors = []
        
        for i in range(1, num_questions + 1):
            text = request.form.get(f'text_{i}', '').strip()
            option1 = request.form.get(f'option1_{i}', '').strip()
            option2 = request.form.get(f'option2_{i}', '').strip()
            option3 = request.form.get(f'option3_{i}', '').strip()
            option4 = request.form.get(f'option4_{i}', '').strip()
            correct_option = request.form.get(f'correct_option_{i}', '').strip()
            category_id = request.form.get(f'category_{i}', '').strip()
            difficulty = request.form.get(f'difficulty_{i}', '').strip()
            explanation = request.form.get(f'explanation_{i}', '').strip()
            
            # Skip empty questions
            if not text or not option1 or not option2 or not correct_option:
                if text or option1 or option2:  # Partially filled
                    errors.append(f'Question {i}: Missing required fields')
                continue
            
            try:
                q = Question(
                    text=text,
                    option1=option1,
                    option2=option2,
                    option3=option3 if option3 else None,
                    option4=option4 if option4 else None,
                    correct_option=int(correct_option),
                    explanation=explanation if explanation else None,
                    category_id=int(category_id) if category_id else None,
                    difficulty=difficulty if difficulty else None
                )
                db.session.add(q)
                added_count += 1
            except Exception as e:
                errors.append(f'Question {i}: {str(e)}')
        
        if added_count > 0:
            db.session.commit()
            flash(f'{added_count} question(s) added successfully!', 'success')
        if errors:
            for error in errors:
                flash(error, 'warning')
        
        if added_count == 0 and not errors:
            flash('No questions were added. Please fill at least one complete question.', 'warning')
        
        return redirect(url_for('admin.index'))
    
    return render_template('admin/bulk_add_questions.html', categories=cats)

@admin_bp.route('/feedback')
@login_required
@admin_required
def feedback():
    from app.models import Feedback
    try:
        feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    except Exception as e:
        flash(f'Error loading feedback: {str(e)}. Please run "python update_db.py" to create the feedback table.', 'danger')
        feedbacks = []
    return render_template('admin/feedback.html', feedbacks=feedbacks)