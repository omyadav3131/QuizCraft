"""
HEADER_COMMENT_AUTOGEN
FILE: app\quiz\routes.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

# app/quiz/routes.py
from flask import render_template, request, redirect, url_for, session, flash, jsonify, abort
from flask_login import login_required, current_user
from . import quiz_bp
from app.models import Category, Question, Attempt, User, Role, db

def _calculate_quiz_score(answer_map):
    """Recompute quiz score from stored answers using canonical Question data."""
    if not answer_map:
        return 0

    # Fetch all relevant questions in a single query to keep lookups efficient.
    question_ids = [int(q_id) for q_id in answer_map.keys()]
    questions = Question.query.filter(Question.id.in_(question_ids)).all()
    question_lookup = {str(question.id): question for question in questions}

    score = 0
    for q_id_str, chosen_option in answer_map.items():
        question = question_lookup.get(q_id_str)
        try:
            chosen_value = int(chosen_option) if chosen_option is not None else None
        except (TypeError, ValueError):
            chosen_value = None

        if question and chosen_value == question.correct_option:
            score += 1

    return score

@quiz_bp.route('/select')
@login_required
def select():
    # Prevent admin from playing quizzes
    if current_user.is_admin():
        flash('Admin users cannot play quizzes. Please use the admin panel to manage questions.', 'warning')
        return redirect(url_for('admin.index'))
    
    categories = Category.query.order_by(Category.name).all()
    return render_template('quiz/select.html', categories=categories)

@quiz_bp.route('/start/<int:category_id>')
@login_required
def start(category_id):
    # Prevent admin from playing quizzes
    if current_user.is_admin():
        flash('Admin users cannot play quizzes. Please use the admin panel to manage questions.', 'warning')
        return redirect(url_for('admin.index'))
    
    category = Category.query.get_or_404(category_id)
    return render_template('quiz/select_difficulty.html', category=category)

@quiz_bp.route('/start/<int:category_id>/<difficulty>')
@login_required
def start_quiz(category_id, difficulty):
    # Prevent admin from playing quizzes
    if current_user.is_admin():
        flash('Admin users cannot play quizzes. Please use the admin panel to manage questions.', 'warning')
        return redirect(url_for('admin.index'))
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
    from datetime import datetime, timedelta
    session['quiz_category_id'] = str(category_id)
    session['quiz_difficulty'] = difficulty
    session['quiz_questions'] = [str(q.id) for q in questions]
    session['current_question_index'] = 0
    session['quiz_score'] = 0
    session['quiz_answers'] = {}

    # Set quiz start time and end time (10 minutes = 600 seconds)
    session['quiz_start_time'] = datetime.utcnow().isoformat()
    session['quiz_end_time'] = (datetime.utcnow() + timedelta(minutes=10)).isoformat()
    return redirect(url_for('quiz.question', q_id=questions[0].id))

@quiz_bp.route('/question/<int:q_id>', methods=['GET', 'POST'])
@login_required
def question(q_id):
    if 'quiz_questions' not in session:
        flash('Please select a category first', 'warning')
        return redirect(url_for('quiz.select'))
    
    quiz_questions = session['quiz_questions']
    q_id_str = str(q_id)
    if q_id_str not in quiz_questions:
        flash('Invalid question', 'danger')
        return redirect(url_for('quiz.select'))

    current_index = quiz_questions.index(q_id_str)
    session['current_question_index'] = current_index

    answers = dict(session.get('quiz_answers', {}))
    session['quiz_answers'] = answers
    session['quiz_score'] = _calculate_quiz_score(answers)

    # Check if time is up
    if 'quiz_end_time' in session:
        from datetime import datetime
        end_time = datetime.fromisoformat(session['quiz_end_time'])
        if datetime.utcnow() >= end_time:
            flash('Time is up! Quiz will be submitted automatically.', 'warning')
            return redirect(url_for('quiz.result'))

    q = Question.query.get_or_404(q_id)

    if request.method == 'POST':
        action = request.form.get('action', 'next')
        selected_option_raw = request.form.get('option')

        if selected_option_raw:
            try:
                answers[q_id_str] = int(selected_option_raw)
            except (TypeError, ValueError):
                flash('Invalid option selected.', 'danger')
                return redirect(url_for('quiz.question', q_id=q_id))
            session['quiz_answers'] = answers
            session['quiz_score'] = _calculate_quiz_score(answers)

        if action in ('next', 'submit') and q_id_str not in answers:
            flash('Please select an option before proceeding.', 'warning')
            return redirect(url_for('quiz.question', q_id=q_id))

        if action == 'previous':
            target_index = max(0, current_index - 1)
            session['current_question_index'] = target_index
            target_q_id = int(quiz_questions[target_index])
            return redirect(url_for('quiz.question', q_id=target_q_id))

        if current_index >= len(quiz_questions) - 1 or action == 'submit':
            return redirect(url_for('quiz.result'))

        target_index = current_index + 1
        session['current_question_index'] = target_index
        target_q_id = int(quiz_questions[target_index])
        return redirect(url_for('quiz.question', q_id=target_q_id))

    # GET request - show question
    from datetime import datetime
    time_remaining = 600
    if 'quiz_end_time' in session:
        end_time = datetime.fromisoformat(session['quiz_end_time'])
        remaining = (end_time - datetime.utcnow()).total_seconds()
        time_remaining = max(0, int(remaining))

    selected_option = answers.get(q_id_str)

    return render_template(
        'quiz/question.html',
        question=q,
        question_num=current_index + 1,
        total=len(quiz_questions),
        time_remaining=time_remaining,
        selected_option=selected_option,
        has_previous=current_index > 0,
        is_last_question=current_index == len(quiz_questions) - 1
    )

@quiz_bp.route('/result')
@login_required
def result():
    if 'quiz_score' not in session:
        flash('No quiz session found', 'warning')
        return redirect(url_for('quiz.select'))
    
    # Get all session values BEFORE clearing
    quiz_questions = session.get('quiz_questions', [])
    quiz_answers = session.get('quiz_answers', {})
    score = _calculate_quiz_score(quiz_answers)
    total = len(quiz_questions)
    category_id = session.get('quiz_category_id')
    difficulty = session.get('quiz_difficulty', None)

    # Persist the recomputed score for downstream reads (e.g., template flashes)
    session['quiz_score'] = score
    
    # Calculate points based on difficulty: Easy=2, Medium=4, Hard=6
    points_per_question = 0
    if difficulty:
        if difficulty.lower() == 'easy':
            points_per_question = 2
        elif difficulty.lower() == 'medium':
            points_per_question = 4
        elif difficulty.lower() == 'hard':
            points_per_question = 6
    
    total_points = score * points_per_question
    
    # Initialize answer_review_data for display
    answer_review_data = []
    cat_id = None
    
    # Save attempt to database
    if category_id:
        # Convert category_id back to int if it's a string
        cat_id = int(category_id) if isinstance(category_id, str) else category_id

        # Check for recent duplicate attempt (within 10 seconds)
        from datetime import datetime, timedelta
        recent_attempt = Attempt.query.filter_by(
            user_id=current_user.id,
            category_id=cat_id,
            total=total,
            score=score
        ).filter(Attempt.created_at >= datetime.utcnow() - timedelta(seconds=10)).first()

        if not recent_attempt:
            # create and save Attempt
            attempt = Attempt(
                user_id=current_user.id,
                score=score,
                total=total,
                points=total_points,
                category_id=cat_id,
                difficulty=difficulty
            )
            db.session.add(attempt)
            db.session.flush()  # Get attempt.id before commit
            
            # Save individual answers to AttemptAnswer table for review
            from app.models import AttemptAnswer
            answer_review_data = []
            
            for q_id_str in quiz_questions:
                q_id = int(q_id_str)
                question = Question.query.get(q_id)
                if question:
                    chosen_option = quiz_answers.get(q_id_str, 0)
                    is_correct = (chosen_option == question.correct_option)
                    
                    # Save to database
                    attempt_answer = AttemptAnswer(
                        attempt_id=attempt.id,
                        question_id=q_id,
                        chosen_option=chosen_option,
                        correct=is_correct
                    )
                    db.session.add(attempt_answer)
                    
                    # Prepare data for review display
                    answer_review_data.append({
                        'question': question,
                        'chosen_option': chosen_option,
                        'correct_option': question.correct_option,
                        'is_correct': is_correct,
                        'points_earned': points_per_question if is_correct else 0,
                        'explanation': question.explanation
                    })
            
            db.session.commit()

            # Save LeaderboardEntry
            try:
                # username fallback for guests
                username = current_user.username if current_user.is_authenticated else "Guest"

                from app.models import LeaderboardEntry  # local import to avoid circular issues

                lb = LeaderboardEntry(
                    user_id = current_user.id if current_user.is_authenticated else None,
                    username = username,
                    score = score,
                    total = total,
                    points = total_points,
                    category_id = cat_id,
                    difficulty = difficulty
                )
                db.session.add(lb)
                db.session.commit()
            except Exception as e:
                # don't break the user flow if leaderboard insert fails; log if you have logger
                db.session.rollback()
                print("Leaderboard insert error:", e)

    else:
        # If no category_id, still prepare answer review data from session
        for q_id_str in quiz_questions:
            q_id = int(q_id_str)
            question = Question.query.get(q_id)
            if question:
                chosen_option = quiz_answers.get(q_id_str, 0)
                is_correct = (chosen_option == question.correct_option)
                
                answer_review_data.append({
                    'question': question,
                    'chosen_option': chosen_option,
                    'correct_option': question.correct_option,
                    'is_correct': is_correct,
                    'points_earned': points_per_question if is_correct else 0,
                    'explanation': question.explanation
                })


    
    # Clear quiz session AFTER saving everything
    session.pop('quiz_category_id', None)
    session.pop('quiz_difficulty', None)
    session.pop('quiz_questions', None)
    session.pop('current_question_index', None)
    session.pop('quiz_answers', None)
    session.pop('quiz_start_time', None)
    session.pop('quiz_end_time', None)
    session.pop('quiz_score', None)
    
    # Prepare data for result page
    return render_template('quiz/result.html', 
                         score=score, 
                         total=total, 
                         points=total_points, 
                         difficulty=difficulty or 'N/A', 
                         category_id=cat_id,
                         answer_review=answer_review_data,
                         points_per_question=points_per_question)

# Old leaderboard route - commented out, replaced by leaderboard() below (vertical card-style)
# @quiz_bp.route('/leaderboard')
# def leaderboard():
#     """Enhanced leaderboard route with filters"""
#     # Get filter parameters
#     category_id = request.args.get('category', type=int)
#     difficulty = request.args.get('difficulty', type=str)
#     
#     # Build query with joins
#     query = db.session.query(Attempt, User, Category).join(
#         User, Attempt.user_id == User.id
#     ).outerjoin(
#         Category, Attempt.category_id == Category.id
#     )
#     
#     # Apply filters
#     if category_id:
#         query = query.filter(Attempt.category_id == category_id)
#     if difficulty:
#         query = query.filter(Attempt.difficulty == difficulty)
#     
#     # Order by score descending, then by date
#     query = query.order_by(Attempt.score.desc(), Attempt.created_at.desc())
#     
#     # Get all attempts (for top-3 and table)
#     attempts_data = query.limit(100).all()
#     
#     # Get categories for filter dropdown
#     categories = Category.query.order_by(Category.name).all()
#     
#     # Process attempts data
#     attempts_list = []
#     for attempt, user, category in attempts_data:
#         percentage = (attempt.score / attempt.total * 100) if attempt.total and attempt.total > 0 else 0
#         attempts_list.append({
#             'id': attempt.id,
#             'username': user.username if user else 'Unknown',
#             'score': attempt.score,
#             'total': attempt.total,
#             'percentage': round(percentage, 1),
#             'category': category.name if category else 'N/A',
#             'difficulty': attempt.difficulty or 'N/A',
#             'created_at': attempt.created_at.strftime('%Y-%m-%d %H:%M') if attempt.created_at else 'N/A'
#         })
#     
#     # Get top 3 for medals
#     top_3 = attempts_list[:3] if len(attempts_list) >= 3 else attempts_list
#     
#     return render_template('quiz/leaderboard_v2.html', 
#                          attempts=attempts_list,
#                          top_3=top_3,
#                          categories=categories,
#                          selected_category=category_id,
#                          selected_difficulty=difficulty)

@quiz_bp.route('/api/leaderboard')
def api_leaderboard():
    """JSON API endpoint for leaderboard data"""
    category_id = request.args.get('category', type=int)
    difficulty = request.args.get('difficulty', type=str)
    limit = request.args.get('limit', type=int, default=50)
    
    # Build query
    query = db.session.query(Attempt, User, Category).join(
        User, Attempt.user_id == User.id
    ).outerjoin(
        Category, Attempt.category_id == Category.id
    )
    
    # Apply filters
    if category_id:
        query = query.filter(Attempt.category_id == category_id)
    if difficulty:
        query = query.filter(Attempt.difficulty == difficulty)
    
    # Order and limit
    query = query.order_by(Attempt.score.desc(), Attempt.created_at.desc()).limit(limit)
    
    attempts_data = query.all()
    
    result = []
    for attempt, user, category in attempts_data:
        percentage = (attempt.score / attempt.total * 100) if attempt.total and attempt.total > 0 else 0
        result.append({
            'id': attempt.id,
            'username': user.username if user else 'Unknown',
            'score': attempt.score,
            'total': attempt.total,
            'percentage': round(percentage, 1),
            'category': category.name if category else 'N/A',
            'difficulty': attempt.difficulty or 'N/A',
            'created_at': attempt.created_at.isoformat() if attempt.created_at else None
        })
    
    return jsonify({
        'success': True,
        'count': len(result),
        'data': result
    })

@quiz_bp.route('/leaderboard')
@login_required
def leaderboard():
    from app.models import Attempt, User, Category
    from datetime import datetime, timedelta
    
    # Get filter parameters from query params
    category_id = request.args.get('category', type=int)
    date_filter = request.args.get('date_filter', default='today', type=str)  # today, week, month, all
    
    # Get all categories for filter dropdown
    categories = Category.query.order_by(Category.name).all()
    
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

    q = (
        db.session.query(
            Attempt,
            User.username,
            Category.name.label("category_name")
        )
        .outerjoin(User, User.id == Attempt.user_id)
        .outerjoin(Category, Category.id == Attempt.category_id)
        .filter(Attempt.created_at >= from_date)
        .filter(Attempt.created_at <= to_date)
    )
    
    # Filter by category if provided
    if category_id:
        q = q.filter(Attempt.category_id == category_id)
    
    # Order by points (descending), then by score, then by date
    from sqlalchemy import inspect
    inspector = inspect(Attempt)
    has_points_column = 'points' in [col.name for col in inspector.columns]
    
    if has_points_column:
        q = q.order_by(Attempt.points.desc(), Attempt.score.desc(), Attempt.created_at.desc()).limit(50)
    else:
        q = q.order_by(Attempt.score.desc(), Attempt.created_at.desc()).limit(50)

    rows = q.all()

    entries = []
    for attempt, username, category_name in rows:
        entries.append({
            "username": username or "Guest",
            "score": attempt.score,
            "total": attempt.total,
            "points": getattr(attempt, 'points', 0) or 0,
            "category": category_name or "General",
            "difficulty": attempt.difficulty or "N/A",
            "date": attempt.created_at.strftime("%Y-%m-%d"),
        })

    return render_template("quiz/leaderboard_vertical.html", entries=entries, 
                         categories=categories, selected_category=category_id, date_filter=date_filter)

@quiz_bp.route('/leaderboard/<category_name>')
@login_required
def leaderboard_category(category_name):
    from app.models import Attempt, User, Category
    
    # Find category by name (case-insensitive)
    category = Category.query.filter(Category.name.ilike(f'%{category_name}%')).first_or_404()
    
    # Get all categories for filter dropdown
    categories = Category.query.order_by(Category.name).all()

    q = (
        db.session.query(
            Attempt,
            User.username,
            Category.name.label("category_name")
        )
        .outerjoin(User, User.id == Attempt.user_id)
        .outerjoin(Category, Category.id == Attempt.category_id)
        .filter(Attempt.category_id == category.id)
        # Check if points column exists for ordering
        .order_by(Attempt.score.desc(), Attempt.created_at.desc())
        .limit(50)
    )

    rows = q.all()

    entries = []
    for attempt, username, cat_name in rows:
        entries.append({
            "username": username or "Guest",
            "score": attempt.score,
            "total": attempt.total,
            "points": getattr(attempt, 'points', 0) or 0,
            "category": cat_name or "General",
            "difficulty": attempt.difficulty or "N/A",
            "date": attempt.created_at.strftime("%Y-%m-%d"),
        })

    return render_template("quiz/leaderboard_vertical.html", entries=entries, 
                         categories=categories, selected_category=category.id, category_name=category.name)

@quiz_bp.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    from app.models import Feedback
    
    if request.method == 'GET':
        # Show feedback form
        return render_template('quiz/feedback.html')
    
    # POST - Submit feedback
    name = request.form.get('name', '').strip()
    rating = request.form.get('rating', type=int)
    feedback_text = request.form.get('feedback_text', '').strip()
    
    if not name or not rating or not feedback_text:
        flash('Please fill in all fields', 'warning')
        return render_template('quiz/feedback.html')
    
    # Create feedback entry
    feedback_entry = Feedback(
        user_id=current_user.id if current_user.is_authenticated else None,
        name=name,
        rating=rating,
        feedback_text=feedback_text
    )
    
    db.session.add(feedback_entry)
    db.session.commit()
    
    flash('Thank you for your feedback!', 'success')
    return redirect(url_for('quiz.feedback'))

@quiz_bp.route('/performance')
@login_required
def performance_dashboard():
    from datetime import datetime, timedelta
    from app.models import Competition, CompetitionAttempt

    requested_user_id = request.args.get('user_id', type=int)

    if current_user.is_admin():
        if not requested_user_id:
            flash('कृपया किसी उपयोगकर्ता को चुनें ताकि उसका परफॉर्मेंस देखा जा सके।', 'warning')
            return redirect(url_for('admin.user_progress'))

        target_user = User.query.filter(
            User.id == requested_user_id,
            User.role == Role.USER
        ).first()

        if not target_user:
            flash('यह उपयोगकर्ता उपलब्ध नहीं है या उसे देखा नहीं जा सकता।', 'warning')
            return redirect(url_for('admin.user_progress'))
    else:
        if requested_user_id and requested_user_id != current_user.id:
            abort(403)
        target_user = current_user

    # Get all attempts for selected user
    attempts = Attempt.query.filter_by(user_id=target_user.id).order_by(Attempt.created_at).all()

    # Get all competition attempts for selected user
    comp_attempts = (
        CompetitionAttempt.query.filter_by(user_id=target_user.id)
        .order_by(CompetitionAttempt.started_at)
        .all()
    )
    
    # Get all categories for display
    all_categories = Category.query.all()

    if not attempts and not comp_attempts:
        return render_template(
            'quiz/performance.html',
            attempts=[],
            score_data=[],
            points_data=[],
            total_quizzes=0,
            avg_score=0,
            total_points=0,
            comp_attempts=comp_attempts,
            comp_total_attempts=0,
            comp_avg_score=0,
            categories=all_categories
        )

    # Prepare data for quiz charts
    score_data = []
    points_data = []
    
    for attempt in attempts:
        # Score over time
        score_data.append({
            'date': attempt.created_at.strftime('%Y-%m-%d'),
            'score': attempt.score,
            'total': attempt.total,
            'percentage': round((attempt.score / attempt.total * 100) if attempt.total > 0 else 0, 1)
        })
        
        # Points over time
        points_data.append({
            'date': attempt.created_at.strftime('%Y-%m-%d'),
            'points': attempt.points or 0
        })
    
    # Calculate competition statistics
    comp_total_attempts = len(comp_attempts)
    comp_total_score = sum(ca.correct_answers for ca in comp_attempts) if comp_attempts else 0
    comp_total_questions = sum(ca.total_questions for ca in comp_attempts) if comp_attempts else 0
    comp_avg_score = round((comp_total_score / comp_total_questions * 100) if comp_total_questions > 0 else 0, 1)
    
    # Overall statistics
    total_quizzes = len(attempts)
    total_score = sum(a.score for a in attempts)
    total_questions = sum(a.total for a in attempts)
    avg_score = round((total_score / total_questions * 100) if total_questions > 0 else 0, 1)
    total_points = sum(a.points or 0 for a in attempts)
    
    return render_template('quiz/performance.html',
                         attempts=attempts,
                         score_data=score_data,
                         points_data=points_data,
                         total_quizzes=total_quizzes,
                         avg_score=avg_score,
                         total_points=total_points,
                         comp_attempts=comp_attempts,
                         comp_total_attempts=comp_total_attempts,
                         comp_avg_score=comp_avg_score,
                         categories=all_categories)