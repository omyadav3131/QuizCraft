import secrets
import string
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

    user_competitions = Competition.query.filter(
        (Competition.creator_id == current_user.id) | 
        (Competition.user_attempts.any(CompetitionAttempt.user_id == current_user.id))
    ).all()
    return render_template('competition/competition_menu.html', competitions=user_competitions)


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
    
    comp.status = 'in_progress'
    comp.started_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Competition started!'})


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
    
    # Get questions for this competition
    questions = Question.query.filter_by(
        category_id=comp.category_id,
        difficulty=comp.difficulty
    ).limit(comp.num_questions).all()
    
    if not questions:
        flash('No questions available for this competition', 'error')
        return redirect(url_for('competition.competition_menu'))
    
    current_question_index = request.args.get('q', 0, type=int)
    
    if current_question_index >= len(questions):
        return redirect(url_for('competition.submit_competition_test', code=code))
    
    question = questions[current_question_index]
    
    print(f"DEBUG: Taking test - Q{current_question_index + 1}/{len(questions)}, User: {current_user.username}")
    
    return render_template('competition/test.html', 
                         competition=comp, 
                         question=question,
                         question_index=current_question_index,
                         total_questions=len(questions))


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
        
        # Store answer
        if not user_attempt.answers:
            user_attempt.answers = {}
        
        user_attempt.answers[str(question_id)] = selected_option
        db.session.commit()
        
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
        
        # Get questions and calculate score
        questions = Question.query.filter_by(
            category_id=comp.category_id,
            difficulty=comp.difficulty
        ).limit(comp.num_questions).all()
        
        if not questions:
            flash('No questions found for scoring', 'error')
            return redirect(url_for('competition.competition_menu')), 404
        
        correct_count = 0
        for question in questions:
            selected = user_attempt.answers.get(str(question.id)) if user_attempt.answers else None
            if selected and selected == question.correct_option:
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
    
    return render_template('competition/results.html', 
                         competition=comp, 
                         attempts=attempts)
