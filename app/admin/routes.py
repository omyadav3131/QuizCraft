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
from app.models import db, Question, Category, User, Competition, CompetitionAttempt, Attempt, AttemptAnswer, LeaderboardEntry, Role

from sqlalchemy import func, case, and_, or_
from datetime import datetime, timedelta

@admin_bp.route('/profile')
@login_required
def admin_profile():
    questions_count = Question.query.count()
    competitions_count = Competition.query.count()
    users_count = User.query.count()
    return render_template('admin/profile.html', questions_count=questions_count, competitions_count=competitions_count, users_count=users_count)

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
    # Only show completed competitions
    competitions = Competition.query.filter(
        Competition.created_at >= from_date,
        Competition.created_at <= to_date,
        Competition.status == 'completed'
    ).order_by(Competition.created_at.desc()).all()
    
    # Prepare detailed competition data
    comp_data = []
    for comp in competitions:
        # Get creator and participants with null checks
        creator = User.query.get(comp.creator_id)
        attempts = CompetitionAttempt.query.filter_by(competition_id=comp.id).all()
        participants = []
        for att in attempts:
            user = User.query.get(att.user_id)
            if user:  # Only add if user exists
                participants.append(user)
        
        # Calculate winner with null check
        winner = User.query.get(comp.winner_id) if comp.winner_id else None
        winner_name = winner.username if winner else 'N/A'
        
        # Get scores with null checks
        scores = []
        for att in attempts:
            user = User.query.get(att.user_id)
            if user:  # Only add if user exists
                scores.append((user.username, att.correct_answers, att.total_questions))
        
        comp_data.append({
            'id': comp.id,
            'code': comp.code,
            'category': comp.category.name if comp.category else 'N/A',
            'difficulty': comp.difficulty,
            'creator': creator.username if creator else 'Deleted User',
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

        # Check email uniqueness (only if email is provided and different from current)
        if email and email != u.email:
            other_email = User.query.filter_by(email=email).first()
            if other_email and other_email.id != u.id:
                flash('Email already taken by another user', 'warning')
                return redirect(url_for('admin.edit_user', user_id=u.id))
        
        u.email = email
        u.role = role
        if password:
            u.set_password(password)

        db.session.commit()
        flash('User updated', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user_form.html', user=u)


@admin_bp.route('/user/change-password/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def change_user_password(user_id):
    """Change user password - Admin only"""
    u = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not new_password:
            flash('Password is required', 'warning')
            return redirect(url_for('admin.change_user_password', user_id=user_id))
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long', 'warning')
            return redirect(url_for('admin.change_user_password', user_id=user_id))
        
        if new_password != confirm_password:
            flash('Passwords do not match', 'warning')
            return redirect(url_for('admin.change_user_password', user_id=user_id))
        
        u.set_password(new_password)
        db.session.commit()
        flash(f'Password changed successfully for user: {u.username}', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/change_password.html', user=u)


@admin_bp.route('/user/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    u = User.query.get_or_404(user_id)
    # Prevent deleting own account
    if u.id == current_user.id:
        flash('You cannot delete your own account', 'warning')
        return redirect(url_for('admin.users'))

    # Delete competitions created by this user first (to avoid foreign key constraint error)
    competitions_created = Competition.query.filter_by(creator_id=u.id).all()
    for comp in competitions_created:
        # Delete all attempts for this competition first
        CompetitionAttempt.query.filter_by(competition_id=comp.id).delete()
        db.session.delete(comp)
    
    # Delete competition attempts by this user
    CompetitionAttempt.query.filter_by(user_id=u.id).delete()
    
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

@admin_bp.route('/user-progress')
@login_required
@admin_required
def user_progress():
    """Display platform-wide user analytics with quick competition snapshot."""

    one_week_ago = datetime.utcnow() - timedelta(days=7)

    total_users = User.query.filter(User.role == Role.USER).count()

    active_this_week = (
        db.session.query(func.count(func.distinct(Attempt.user_id)))
        .join(User, User.id == Attempt.user_id)
        .filter(Attempt.created_at >= one_week_ago, User.role == Role.USER)
        .scalar() or 0
    )

    total_attempts = (
        db.session.query(func.count(Attempt.id))
        .join(User, User.id == Attempt.user_id)
        .filter(User.role == Role.USER)
        .scalar() or 0
    )

    average_score_query = (
        db.session.query(
            func.avg((Attempt.score * 100.0) / func.nullif(Attempt.total, 0))
        )
        .join(User, User.id == Attempt.user_id)
        .filter(
            Attempt.total.isnot(None),
            Attempt.total > 0,
            User.role == Role.USER
        )
        .scalar()
    )

    average_score = round(average_score_query or 0, 2)

    competitions_tracked = Competition.query.count()
    participants_count = (
        db.session.query(func.count(func.distinct(CompetitionAttempt.user_id)))
        .join(User, User.id == CompetitionAttempt.user_id)
        .filter(User.role == Role.USER)
        .scalar() or 0
    )

    user_rows = (
        db.session.query(
            User.id,
            User.username,
            func.count(Attempt.id).label('attempts'),
            func.coalesce(
                func.avg((Attempt.score * 100.0) / func.nullif(Attempt.total, 0)),
                0
            ).label('avg_score'),
            func.max(Attempt.created_at).label('last_activity'),
        )
        .outerjoin(Attempt, Attempt.user_id == User.id)
        .filter(User.role == Role.USER)
        .group_by(User.id, User.username)
        .order_by(User.username.asc())
    ).all()

    users = [
        {
            'id': row.id,
            'username': row.username,
            'attempts': row.attempts,
            'avg_score': round(row.avg_score or 0, 2),
            'last_activity': row.last_activity,
        }
        for row in user_rows
    ]

    competition_rows = (
        db.session.query(
            Competition.id,
            Competition.code,
            Category.name.label('category_name'),
            Competition.difficulty,
            Competition.started_at,
            Competition.created_at,
            func.count(func.distinct(CompetitionAttempt.user_id)).label('participants'),
            func.coalesce(func.avg(CompetitionAttempt.score), 0).label('avg_score'),
        )
        .outerjoin(Category, Competition.category_id == Category.id)
        .outerjoin(CompetitionAttempt, CompetitionAttempt.competition_id == Competition.id)
        .outerjoin(User, User.id == CompetitionAttempt.user_id)
        .group_by(
            Competition.id,
            Competition.code,
            Category.name,
            Competition.difficulty,
            Competition.started_at,
            Competition.created_at,
        )
        .filter((User.id == None) | (User.role == Role.USER))
        .order_by(Competition.created_at.desc())
        .limit(20)
    ).all()

    competitions = [
        {
            'id': row.id,
            'code': row.code,
            'category': row.category_name or 'N/A',
            'difficulty': row.difficulty,
            'participants': row.participants,
            'avg_score': round(row.avg_score or 0, 2),
            'started_at': row.started_at or row.created_at,
        }
        for row in competition_rows
    ]

    return render_template(
        'admin/user_progress.html',
        total_users=total_users,
        active_this_week=active_this_week,
        total_attempts=total_attempts,
        average_score=average_score,
        competitions_tracked=competitions_tracked,
        participants_count=participants_count,
        users=users,
        competitions=competitions,
    )


@admin_bp.route('/user/<int:user_id>/progress')
@login_required
@admin_required
def user_progress_detail(user_id):
    """Drill-down analytics for a single user's activity."""

    user = User.query.get_or_404(user_id)

    attempt_records = (
        db.session.query(
            Attempt.id,
            Attempt.created_at,
            Attempt.score,
            Attempt.total,
            Attempt.points,
            Attempt.difficulty,
            Category.name.label('category_name'),
        )
        .outerjoin(Category, Attempt.category_id == Category.id)
        .filter(Attempt.user_id == user.id)
        .order_by(Attempt.created_at.desc())
        .all()
    )

    total_attempts = len(attempt_records)

    avg_score_query = (
        db.session.query(
            func.avg((Attempt.score * 100.0) / func.nullif(Attempt.total, 0))
        )
        .filter(Attempt.user_id == user.id, Attempt.total.isnot(None), Attempt.total > 0)
        .scalar()
    )
    avg_score = round(avg_score_query or 0, 2)

    attempts = []
    for record in attempt_records:
        if record.total:
            score_pct = round((record.score * 100.0) / record.total, 2)
        else:
            score_pct = 0.0
        attempts.append(
            {
                'id': record.id,
                'created_at': record.created_at,
                'category_name': record.category_name or 'General',
                'difficulty': record.difficulty or 'N/A',
                'score': record.score or 0,
                'total': record.total or 0,
                'score_pct': score_pct,
                'points': record.points or 0,
            }
        )

    timeseries = [
        {
            'date': attempt['created_at'].strftime('%Y-%m-%d'),
            'score': attempt['score_pct'],
            'label': attempt['category_name'],
        }
        for attempt in sorted(attempts, key=lambda item: item['created_at'])
    ]

    return render_template(
        'admin/user_progress_detail.html',
        user=user,
        attempts=attempts,
        timeseries=timeseries,
        total_attempts=total_attempts,
        avg_score=avg_score,
    )


@admin_bp.route('/user/<int:user_id>/performance')
@login_required
@admin_required
def admin_user_performance(user_id):
    """Allow admins to open the standard user performance dashboard for any user."""

    user = User.query.get_or_404(user_id)
    performance_url = url_for('quiz.performance_dashboard', user_id=user.id)
    return redirect(performance_url)