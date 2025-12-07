import secrets
import string
import time
import json
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Competition, CompetitionAttempt, Question, Category
from . import competition_bp


def generate_competition_code():
    """Generate unique 8-character alphanumeric code"""
    characters = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(secrets.choice(characters) for _ in range(8))
        if not Competition.query.filter_by(code=code).first():
            return code


@competition_bp.route('/')
@login_required
def competition_menu():
    """Main competition hub"""
    # Auto-remove competitions stuck in 'waiting' for >3 minutes
    now = datetime.utcnow()
    stale_cutoff = now.timestamp() - 180  # 3 minutes in seconds
    stale_comps = Competition.query.filter(
        Competition.status == 'waiting',
        Competition.created_at < datetime.utcfromtimestamp(stale_cutoff)
    ).all()
    for comp in stale_comps:
        db.session.delete(comp)
    if stale_comps:
        db.session.commit()

    # Only show competitions that are actionable or completed for the user
    user_competitions = Competition.query.filter(
        ((Competition.creator_id == current_user.id) | 
         (Competition.user_attempts.any(CompetitionAttempt.user_id == current_user.id)))
    ).all()
    filtered_comps = []
    for comp in user_competitions:
        # Hide competitions that are 'waiting' or 'in_progress' and older than 3 minutes
        if comp.status == 'completed':
            filtered_comps.append(comp)
        elif comp.status == 'in_progress':
            # Only show if user has not yet submitted
            user_attempt = next((a for a in comp.user_attempts if a.user_id == current_user.id), None)
            if user_attempt and user_attempt.status != 'completed':
                filtered_comps.append(comp)
        # Optionally, show 'waiting' only if user is creator and it's not stale
        elif comp.status == 'waiting':
            if comp.creator_id == current_user.id:
                # Not stale
                if (now - comp.created_at).total_seconds() < 180:
                    filtered_comps.append(comp)
    return render_template('competition/competition_menu.html', competitions=filtered_comps)


@competition_bp.route('/ping')
def ping():
    return "competition pong"


@competition_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_competition():
    """Create a new competition"""
    if request.method == 'POST':
        category_id = request.form.get('category_id', type=int)
        difficulty = request.form.get('difficulty')
        num_questions = request.form.get('num_questions', 10, type=int)
        time_limit = request.form.get('time_limit', 600, type=int)
        
        # Validate
        if not category_id or difficulty not in ['Easy', 'Medium', 'Hard']:
            flash('Invalid category or difficulty', 'error')
            return redirect(url_for('competition.create_competition'))
        
        # Check question availability
        question_count = Question.query.filter_by(
            category_id=category_id, 
            difficulty=difficulty
        ).count()
        
        if question_count < num_questions:
            flash(f'Only {question_count} questions available. Please select fewer.', 'error')
            return redirect(url_for('competition.create_competition'))
        
        # Create competition
        code = generate_competition_code()
        comp = Competition(
            code=code,
            creator_id=current_user.id,
            category_id=category_id,
            difficulty=difficulty,
            num_questions=num_questions,
            time_limit=time_limit
        )
        db.session.add(comp)
        db.session.commit()
        
        # Create attempt for creator immediately
        creator_attempt = CompetitionAttempt(
            competition_id=comp.id,
            user_id=current_user.id,
            total_questions=num_questions
        )
        db.session.add(creator_attempt)
        db.session.commit()
        
        flash(f'✅ Competition created! Share code: <strong>{code}</strong>', 'success')
        return redirect(url_for('competition.wait_for_opponent', code=code))
    
    categories = Category.query.all()
    return render_template('competition/create.html', categories=categories)


@competition_bp.route('/join', methods=['GET', 'POST'])
@login_required
def join_competition():
    """Join existing competition"""
    if request.method == 'POST':
        code = request.form.get('code', '').upper().strip()
        
        comp = Competition.query.filter_by(code=code).first()
        if not comp:
            flash('❌ Invalid competition code', 'error')
            return redirect(url_for('competition.join_competition'))
        
        # Check if user already joined
        existing = CompetitionAttempt.query.filter_by(
            competition_id=comp.id,
            user_id=current_user.id
        ).first()
        if existing:
            flash('You already joined this competition', 'info')
            return redirect(url_for('competition.wait_for_opponent', code=code))
        
        # Check if full (2 players max)
        attempt_count = CompetitionAttempt.query.filter_by(competition_id=comp.id).count()
        if attempt_count >= 2:
            flash('❌ Competition is full (max 2 players)', 'error')
            return redirect(url_for('competition.join_competition'))
        
        # Check if creator is trying to join themselves
        if comp.creator_id == current_user.id:
            flash('❌ Creator cannot join their own competition', 'error')
            return redirect(url_for('competition.join_competition'))
        
        # Add attempt for this user
        attempt = CompetitionAttempt(
            competition_id=comp.id,
            user_id=current_user.id,
            total_questions=comp.num_questions
        )
        db.session.add(attempt)
        db.session.commit()
        
        flash(f'✅ Joined competition! Code: {code}', 'success')
        return redirect(url_for('competition.wait_for_opponent', code=code))
    
    return render_template('competition/join.html')


@competition_bp.route('/wait/<code>', methods=['GET'])
@login_required
def wait_for_opponent(code):
    """Wait for opponent to join or start"""
    comp = Competition.query.filter_by(code=code).first()
    if not comp:
        flash('Competition not found', 'error')
        return redirect(url_for('competition.competition_menu'))
    
    is_creator = comp.creator_id == current_user.id
    
    # Count all attempts
    attempts = CompetitionAttempt.query.filter_by(competition_id=comp.id).all()
    opponent_ready = len(attempts) >= 2
    
    print(f"DEBUG: Code={code}, Creator={is_creator}, Attempts={len(attempts)}, Ready={opponent_ready}")
    for att in attempts:
        print(f"  - User: {att.user.username}, ID: {att.user_id}")
    
    return render_template('competition/wait.html', 
                         competition=comp, 
                         opponent_ready=opponent_ready,
                         is_creator=is_creator)


@competition_bp.route('/start/<code>', methods=['POST'])
@login_required
def start_competition(code):
    """Start competition (creator only)"""
    comp = Competition.query.filter_by(code=code).first()
    if not comp:
        return jsonify({'success': False, 'message': 'Competition not found'}), 404
    
    if comp.creator_id != current_user.id:
        return jsonify({'success': False, 'message': 'Only creator can start'}), 403
    
    attempts = CompetitionAttempt.query.filter_by(competition_id=comp.id).all()
    if len(attempts) < 2:
        return jsonify({'success': False, 'message': 'Need 2 players to start'}), 400
    
    # Set started_at timestamp - this will be the same for all players
    # IMPORTANT: Use time.time() FIRST to get exact UTC timestamp, then create datetime from it
    # This ensures consistency when converting back to timestamp later
    start_utc_timestamp = time.time()
    # Create datetime from timestamp to ensure exact match
    start_time = datetime.utcfromtimestamp(start_utc_timestamp)
    comp.status = 'in_progress'
    comp.started_at = start_time
    
    # Reset all attempts' started_at to the same time for consistency
    for attempt in attempts:
        attempt.started_at = start_time
        attempt.answers = {}  # Reset answers
        attempt.status = 'in_progress'
    
    db.session.commit()
    
    # Return the start timestamp in milliseconds for client-side sync
    # Use the SAME timestamp we used to create the datetime
    start_timestamp_ms = int(start_utc_timestamp * 1000)
    
    print(f"DEBUG: Competition started - UTC timestamp: {start_utc_timestamp}, MS: {start_timestamp_ms}, Time limit: {comp.time_limit}s, Datetime: {start_time}")
    
    return jsonify({
        'success': True, 
        'message': 'Competition started!',
        'startTime': start_timestamp_ms,
        'timeLimit': comp.time_limit
    })


@competition_bp.route('/take/<code>', methods=['GET'])
@login_required
def take_competition_test(code):
    """Take the competition test"""
    comp = Competition.query.filter_by(code=code).first()
    if not comp:
        flash('Competition not found', 'error')
        return redirect(url_for('competition.competition_menu'))
    
    user_attempt = CompetitionAttempt.query.filter_by(
        competition_id=comp.id,
        user_id=current_user.id
    ).first()
    
    if not user_attempt:
        flash('You are not part of this competition', 'error')
        return redirect(url_for('competition.competition_menu'))
    
    if comp.status != 'in_progress':
        flash(f'Competition status: {comp.status}. Status should be in_progress.', 'error')
        return redirect(url_for('competition.wait_for_opponent', code=code))
    
    # Get questions for this competition - ORDER BY ID to ensure consistent ordering
    questions = Question.query.filter_by(
        category_id=comp.category_id,
        difficulty=comp.difficulty
    ).order_by(Question.id).limit(comp.num_questions).all()
    
    if not questions:
        flash('No questions available for this competition', 'error')
        return redirect(url_for('competition.competition_menu'))
    
    current_question_index = request.args.get('q', 0, type=int)
    
    if current_question_index >= len(questions):
        return redirect(url_for('competition.submit_competition_test', code=code))
    
    question = questions[current_question_index]
    
    # Load previously saved answer for this question if exists
    saved_answer = None
    if user_attempt.answers:
        if isinstance(user_attempt.answers, dict):
            saved_answer = user_attempt.answers.get(str(question.id))
        elif isinstance(user_attempt.answers, str):
            try:
                import json
                answers_dict = json.loads(user_attempt.answers)
                saved_answer = answers_dict.get(str(question.id))
            except:
                pass
    
    # Calculate remaining time based on competition start time
    # Pass start timestamp in milliseconds for client-side synchronization
    if comp.started_at:
        # Get current UTC timestamp in seconds
        current_utc_timestamp = time.time()
        
        # Convert started_at datetime to UTC timestamp
        # datetime.utcfromtimestamp() creates naive UTC datetime
        # To convert back, we calculate manually to ensure UTC (not local time)
        epoch = datetime(1970, 1, 1)
        # Calculate seconds since epoch for UTC datetime
        start_utc_timestamp = (comp.started_at - epoch).total_seconds()
        
        # Calculate elapsed time (should be >= 0, but allow small negative for timing)
        elapsed_seconds = current_utc_timestamp - start_utc_timestamp
        
        # If elapsed is negative or very small, competition just started
        if elapsed_seconds < 0:
            print(f"INFO: Negative elapsed time ({elapsed_seconds:.2f}s) - competition just started, setting to 0")
            elapsed_seconds = 0
        elif elapsed_seconds < 1:
            # Less than 1 second elapsed, set to 0 for safety
            elapsed_seconds = 0
        
        # Calculate remaining time
        remaining_seconds = max(0, comp.time_limit - int(elapsed_seconds))
        
        # Use calculated UTC timestamp in milliseconds for client
        # This MUST match the timestamp calculation used when starting competition
        start_timestamp_ms = int(start_utc_timestamp * 1000)
        
        print(f"DEBUG: Timer calc - Current UTC: {current_utc_timestamp:.2f}, Start UTC: {start_utc_timestamp:.2f}, Elapsed: {elapsed_seconds:.2f}s, Remaining: {remaining_seconds}s, Start MS: {start_timestamp_ms}")
    else:
        start_timestamp_ms = None
        remaining_seconds = comp.time_limit
        print(f"DEBUG: Competition not started yet, remaining: {remaining_seconds}s")
    
    print(f"DEBUG: Taking test - Q{current_question_index + 1}/{len(questions)}, User: {current_user.username}, Remaining time: {remaining_seconds}s, Start timestamp: {start_timestamp_ms}")
    
    return render_template('competition/test.html', 
                         competition=comp, 
                         question=question,
                         question_index=current_question_index,
                         total_questions=len(questions),
                         questions=questions,  # Pass all questions for reference
                         remaining_seconds=remaining_seconds,
                         start_timestamp_ms=start_timestamp_ms,
                         saved_answer=saved_answer)


@competition_bp.route('/submit-answer/<code>', methods=['POST'])
@login_required
def submit_answer(code):
    """Submit an answer during competition"""
    try:
        data = request.get_json()
        question_id = data.get('question_id')
        selected_option = data.get('selected_option')
        
        if not question_id or selected_option is None:
            return jsonify({'success': False, 'message': 'Missing question_id or selected_option'}), 400
        
        question_id = int(question_id)
        selected_option = int(selected_option)
        
        comp = Competition.query.filter_by(code=code).first()
        if not comp:
            return jsonify({'success': False, 'message': 'Competition not found'}), 404
        
        user_attempt = CompetitionAttempt.query.filter_by(
            competition_id=comp.id,
            user_id=current_user.id
        ).first()
        
        if not user_attempt:
            return jsonify({'success': False, 'message': 'Not part of competition'}), 403
        
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'success': False, 'message': 'Question not found'}), 404
        
        # Store answer - ensure answers dict exists and properly append
        # IMPORTANT: SQLAlchemy JSON columns need explicit dict assignment for updates
        
        # Get current answers or initialize empty dict
        current_answers = {}
        if user_attempt.answers:
            if isinstance(user_attempt.answers, dict):
                current_answers = dict(user_attempt.answers)  # Create a copy
            elif isinstance(user_attempt.answers, str):
                try:
                    current_answers = json.loads(user_attempt.answers)
                except:
                    current_answers = {}
            else:
                current_answers = {}
        
        # Add/update the answer
        current_answers[str(question_id)] = selected_option
        
        # IMPORTANT: Assign the entire dict back to trigger SQLAlchemy change detection
        user_attempt.answers = current_answers
        
        # Force commit to ensure answer is saved before response
        db.session.commit()
        
        # Refresh to get latest state and verify
        db.session.refresh(user_attempt)
        
        # Verify the answer was saved
        saved_answers = user_attempt.answers if isinstance(user_attempt.answers, dict) else {}
        if isinstance(user_attempt.answers, str):
            try:
                saved_answers = json.loads(user_attempt.answers)
            except:
                saved_answers = {}
        
        print(f"DEBUG: Saved answer for user {current_user.username}, Q{question_id} = Option {selected_option}")
        print(f"DEBUG: Total saved answers: {len(saved_answers)}, All answers: {saved_answers}")
        print(f"DEBUG: Verification - Q{question_id} in saved: {str(question_id) in saved_answers}, Value: {saved_answers.get(str(question_id))}")
        
        # Check if correct
        is_correct = selected_option == question.correct_option
        
        return jsonify({
            'success': True,
            'is_correct': is_correct,
            'correct_option': question.correct_option
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@competition_bp.route('/submit/<code>', methods=['POST'])
@login_required
def submit_competition_test(code):
    """Submit completed test and calculate score"""
    try:
        comp = Competition.query.filter_by(code=code).first()
        if not comp:
            flash('Competition not found', 'error')
            return redirect(url_for('competition.competition_menu')), 404
        
        user_attempt = CompetitionAttempt.query.filter_by(
            competition_id=comp.id,
            user_id=current_user.id
        ).first()
        
        if not user_attempt:
            flash('You are not part of this competition', 'error')
            return redirect(url_for('competition.competition_menu')), 403
        
        # Skip if already completed
        if user_attempt.status == 'completed':
            print(f"DEBUG: User {current_user.username} already completed")
            return redirect(url_for('competition.competition_results', code=code))
        
        # Get questions and calculate score - ORDER BY ID to ensure consistent ordering
        questions = Question.query.filter_by(
            category_id=comp.category_id,
            difficulty=comp.difficulty
        ).order_by(Question.id).limit(comp.num_questions).all()
        
        if not questions:
            flash('No questions found for scoring', 'error')
            return redirect(url_for('competition.competition_menu')), 404
        
        correct_count = 0
        
        # IMPORTANT: Properly load answers from JSON column
        answers_dict = {}
        if user_attempt.answers:
            if isinstance(user_attempt.answers, dict):
                answers_dict = user_attempt.answers
            elif isinstance(user_attempt.answers, str):
                try:
                    answers_dict = json.loads(user_attempt.answers)
                except:
                    answers_dict = {}
        
        print(f"DEBUG: Calculating score for {current_user.username}")
        print(f"DEBUG: Total questions: {len(questions)}")
        print(f"DEBUG: Answers type: {type(user_attempt.answers)}")
        print(f"DEBUG: Answers dict: {answers_dict}")
        print(f"DEBUG: Answers dict length: {len(answers_dict)}")
        
        for question in questions:
            selected = answers_dict.get(str(question.id))
            # Also try integer key in case it was stored as int
            if selected is None:
                selected = answers_dict.get(question.id)
            
            print(f"DEBUG: Q{question.id} - Selected: {selected}, Correct: {question.correct_option}, Match: {selected == question.correct_option if selected else False}")
            
            if selected is not None and selected == question.correct_option:
                correct_count += 1
        
        # Update attempt with final scores
        user_attempt.correct_answers = correct_count
        user_attempt.score = (correct_count / len(questions)) * 100 if questions else 0.0
        user_attempt.completed_at = datetime.utcnow()
        user_attempt.status = 'completed'
        user_attempt.time_taken = int((user_attempt.completed_at - user_attempt.started_at).total_seconds())
        
        db.session.commit()
        print(f"DEBUG: {current_user.username} completed with score {user_attempt.score}%")
        
        # Check if both completed → determine winner
        all_attempts = CompetitionAttempt.query.filter_by(competition_id=comp.id).all()
        completed_attempts = [att for att in all_attempts if att.status == 'completed']
        
        if len(completed_attempts) == len(all_attempts) and len(all_attempts) >= 2:
            # All players completed - determine winner
            winner = max(completed_attempts, key=lambda x: x.score)
            comp.winner_id = winner.user_id
            comp.status = 'completed'
            comp.ended_at = datetime.utcnow()
            db.session.commit()
            print(f"DEBUG: Competition completed. Winner: {winner.user.username} with score {winner.score}%")
        
        return redirect(url_for('competition.competition_results', code=code))
    except Exception as e:
        print(f"ERROR in submit_competition_test: {e}")
        flash(f'Error submitting test: {str(e)}', 'error')
        return redirect(url_for('competition.competition_menu')), 500


@competition_bp.route('/results/<code>', methods=['GET'])
@login_required
def competition_results(code):
    """View competition results"""
    comp = Competition.query.filter_by(code=code).first()
    if not comp:
        flash('Competition not found', 'error')
        return redirect(url_for('competition.competition_menu'))
    
    attempts = CompetitionAttempt.query.filter_by(competition_id=comp.id).all()
    
    # Get questions for this competition - ORDER BY ID to ensure consistent ordering
    questions = Question.query.filter_by(
        category_id=comp.category_id,
        difficulty=comp.difficulty
    ).order_by(Question.id).limit(comp.num_questions).all()
    
    # Prepare detailed review data: for each question, show what each user answered
    import json
    review_data = []
    for question in questions:
        question_review = {
            'question': question,
            'user_answers': []
        }
        
        for attempt in attempts:
            # Properly load answers from JSON column
            attempt_answers = {}
            if attempt.answers:
                if isinstance(attempt.answers, dict):
                    attempt_answers = attempt.answers
                elif isinstance(attempt.answers, str):
                    try:
                        attempt_answers = json.loads(attempt.answers)
                    except:
                        attempt_answers = {}
            
            user_answer = attempt_answers.get(str(question.id))
            # Also try integer key
            if user_answer is None:
                user_answer = attempt_answers.get(question.id)
            
            is_correct = (user_answer == question.correct_option) if user_answer is not None else False
            
            # Only add if user exists (handle deleted users)
            if attempt.user:
                question_review['user_answers'].append({
                    'user': attempt.user,
                    'selected_option': user_answer,
                    'is_correct': is_correct
                })
        
        review_data.append(question_review)
    
    return render_template('competition/results.html', 
                         competition=comp, 
                         attempts=attempts,
                         review_data=review_data)
