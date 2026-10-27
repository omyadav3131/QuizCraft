import json
import logging
import random
from datetime import datetime, timedelta, timezone
from flask import render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from app import db, limiter
from app.models import MockTest, MockSection, MockQuestion, MockAttempt, MockAnswer, MockViolation, Role
from . import mock_bp

logger = logging.getLogger(__name__)


def normalize_utc(dt):
    """
    Ensure datetime is timezone-naive in UTC for consistent comparisons.
    Works transparently across SQLite (naive) and PostgreSQL/psycopg2 (aware).
    """
    if dt is None:
        return None
    if getattr(dt, 'tzinfo', None) is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def get_sections_layout(question_order):
    """
    Safely extract sections layout from question_order.
    Handles dict, JSON string, or None.
    """
    if not question_order:
        return []
    if isinstance(question_order, str):
        try:
            parsed = json.loads(question_order)
            if isinstance(parsed, dict):
                return parsed.get('sections', [])
        except Exception:
            return []
    if isinstance(question_order, dict):
        return question_order.get('sections', [])
    return []


def finalize_mock_attempt(attempt, status='completed'):
    """
    Finalize student attempt, calculate score with NO negative marking,
    and persist results safely.
    """
    if attempt.status != 'in_progress':
        return attempt

    attempt.status = status
    attempt.submitted_at = datetime.utcnow()

    total_score = 0
    total_marks = 0

    for section in attempt.test.sections:
        for q in section.questions:
            total_marks += (q.marks or 1)
            ans = MockAnswer.query.filter_by(
                attempt_id=attempt.id,
                question_id=q.id
            ).first()

            if ans and ans.chosen_option is not None and ans.chosen_option == q.correct_option:
                ans.is_correct = True
                total_score += (q.marks or 1)
            else:
                if ans:
                    ans.is_correct = False
                # Rule: No negative marking anywhere: wrong or unanswered = 0 marks.

    attempt.score = total_score
    attempt.total_marks = total_marks
    db.session.commit()
    logger.info("Finalized mock attempt %d for user %s with score %d/%d (status: %s)",
                attempt.id, attempt.user.username, total_score, total_marks, status)
    return attempt


# ──────────────────────────────────────────────────────────────────────────────
# Student Mock Test Routes
# ──────────────────────────────────────────────────────────────────────────────

@mock_bp.route('/')
@mock_bp.route('/tests')
@login_required
def test_list():
    """
    Placement Mocks listing page grouped by company name.
    """
    if current_user.is_admin():
        flash('Admin users should manage tests via the Admin Panel.', 'info')
        return redirect(url_for('admin.mock_tests_list'))

    tests = MockTest.query.filter_by(is_active=True).order_by(
        MockTest.company_name.asc(),
        MockTest.created_at.desc()
    ).all()

    # Group tests by company
    companies = {}
    for test in tests:
        companies.setdefault(test.company_name, []).append(test)

    # Get user's existing attempts map
    user_attempts = MockAttempt.query.filter_by(user_id=current_user.id).all()
    attempts_by_test = {}
    for att in user_attempts:
        # Keep latest attempt per test
        if att.test_id not in attempts_by_test or att.started_at > attempts_by_test[att.test_id].started_at:
            attempts_by_test[att.test_id] = att

    return render_template(
        'mock/tests.html',
        companies=companies,
        attempts_by_test=attempts_by_test
    )


@mock_bp.route('/test/<int:test_id>/instructions')
@login_required
def instructions(test_id):
    """
    Instructions page with section breakdown and mandatory checkbox before Start.
    """
    if current_user.is_admin():
        flash('Admin users cannot take student mock tests.', 'warning')
        return redirect(url_for('admin.mock_tests_list'))

    test = MockTest.query.get_or_404(test_id)
    if not test.is_active:
        flash('This mock test is currently inactive.', 'warning')
        return redirect(url_for('mock.test_list'))

    # Check existing attempt
    latest_attempt = MockAttempt.query.filter_by(
        user_id=current_user.id,
        test_id=test.id
    ).order_by(MockAttempt.started_at.desc()).first()

    has_active_attempt = False
    if latest_attempt:
        if latest_attempt.status == 'in_progress':
            deadline = normalize_utc(latest_attempt.server_deadline)
            if deadline and datetime.utcnow() >= deadline:
                finalize_mock_attempt(latest_attempt, status='timed_out')
            else:
                has_active_attempt = True
        elif not test.allow_multiple_attempts:
            flash('You have already taken this mock test. Viewing your results.', 'info')
            return redirect(url_for('mock.result', attempt_id=latest_attempt.id))

    return render_template(
        'mock/instructions.html',
        test=test,
        latest_attempt=latest_attempt,
        has_active_attempt=has_active_attempt
    )


@mock_bp.route('/test/<int:test_id>/start', methods=['POST'])
@login_required
def start_test(test_id):
    """
    Start or resume a student's mock attempt.
    Enforces server-side deadline, per-student shuffling, and one-attempt rule.
    """
    if current_user.is_admin():
        flash('Admin users cannot take student mock tests.', 'warning')
        return redirect(url_for('admin.mock_tests_list'))

    test = MockTest.query.get_or_404(test_id)
    if not test.is_active:
        flash('This mock test is currently inactive.', 'warning')
        return redirect(url_for('mock.test_list'))

    # Check for existing attempt
    existing_attempt = MockAttempt.query.filter_by(
        user_id=current_user.id,
        test_id=test.id
    ).order_by(MockAttempt.started_at.desc()).first()

    now = datetime.utcnow()

    if existing_attempt:
        if existing_attempt.status == 'in_progress':
            deadline = normalize_utc(existing_attempt.server_deadline)
            if deadline and now >= deadline:
                finalize_mock_attempt(existing_attempt, status='timed_out')
                flash('Your previous attempt expired and has been submitted.', 'info')
                return redirect(url_for('mock.result', attempt_id=existing_attempt.id))
            else:
                # Resume active attempt
                return redirect(url_for('mock.take_test', attempt_id=existing_attempt.id))

        if not test.allow_multiple_attempts and existing_attempt.status in ('completed', 'timed_out', 'disqualified'):
            flash('Multiple attempts are not allowed for this test.', 'warning')
            return redirect(url_for('mock.result', attempt_id=existing_attempt.id))

    # Validate that test has sections and questions
    total_q = test.total_questions_count()
    if total_q == 0:
        flash('This mock test does not have any questions yet. Please check back later.', 'warning')
        return redirect(url_for('mock.test_list'))

    # Build per-student randomized question and option order
    section_data = []
    for section in test.sections:
        q_objs = list(section.questions)
        random.shuffle(q_objs)  # Shuffle question order per student

        q_list = []
        for q in q_objs:
            # Per-question option shuffle (displayed order 1..4)
            opts = [1, 2, 3, 4]
            random.shuffle(opts)
            q_list.append({
                'id': q.id,
                'option_order': opts
            })

        section_data.append({
            'section_id': section.id,
            'name': section.name,
            'questions': q_list
        })

    # Server-side timer deadline
    server_deadline = now + timedelta(minutes=test.duration_minutes)

    new_attempt = MockAttempt(
        user_id=current_user.id,
        test_id=test.id,
        started_at=now,
        server_deadline=server_deadline,
        status='in_progress',
        score=0,
        total_marks=test.total_marks(),
        violation_count=0,
        question_order={'sections': section_data}
    )
    db.session.add(new_attempt)
    db.session.commit()
    logger.info("User %s started MockTest %d (Attempt %d, Deadline: %s)",
                current_user.username, test.id, new_attempt.id, server_deadline.isoformat())

    return redirect(url_for('mock.take_test', attempt_id=new_attempt.id))


@mock_bp.route('/attempt/<int:attempt_id>')
@login_required
def take_test(attempt_id):
    """
    Main exam interface (TCS NQT style).
    Loads student's fixed shuffled question order and saved answers.
    """
    attempt = MockAttempt.query.get_or_404(attempt_id)

    # Security: IDOR verification
    if attempt.user_id != current_user.id:
        abort(403)

    if not attempt.test.is_active:
        flash('This mock test is currently inactive.', 'warning')
        return redirect(url_for('mock.test_list'))

    now = datetime.utcnow()
    deadline = normalize_utc(attempt.server_deadline)

    # Check server-side deadline
    if deadline and now >= deadline:
        finalize_mock_attempt(attempt, status='timed_out')
        flash('Time limit expired! Your test has been submitted automatically.', 'info')
        return redirect(url_for('mock.result', attempt_id=attempt.id))

    if attempt.status != 'in_progress':
        return redirect(url_for('mock.result', attempt_id=attempt.id))

    # Calculate remaining time in seconds
    seconds_remaining = max(0, int((deadline - now).total_seconds())) if deadline else 0

    # Load questions based on saved question_order safely
    sections_layout = get_sections_layout(attempt.question_order)

    # Map question IDs to MockQuestion objects
    all_q_ids = []
    for s in sections_layout:
        for q_entry in s.get('questions', []):
            all_q_ids.append(q_entry['id'])

    if all_q_ids:
        questions_by_id = {q.id: q for q in MockQuestion.query.filter(MockQuestion.id.in_(all_q_ids)).all()}
    else:
        questions_by_id = {}

    # Load existing saved answers
    answers_by_qid = {
        a.question_id: a for a in MockAnswer.query.filter_by(attempt_id=attempt.id).all()
    }

    return render_template(
        'mock/exam.html',
        attempt=attempt,
        test=attempt.test,
        sections_layout=sections_layout,
        questions_by_id=questions_by_id,
        answers_by_qid=answers_by_qid,
        seconds_remaining=seconds_remaining
    )


@mock_bp.route('/attempt/<int:attempt_id>/save', methods=['POST'])
@login_required
@limiter.limit("120/minute")
def save_answer(attempt_id):
    """
    Autosave answer via AJAX on every selection or status change.
    Rejects modification after server-side deadline and triggers auto-submit.
    """
    attempt = MockAttempt.query.get_or_404(attempt_id)

    # IDOR check
    if attempt.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    if not attempt.test.is_active:
        return jsonify({'error': 'This mock test is inactive.'}), 403

    now = datetime.utcnow()
    deadline = normalize_utc(attempt.server_deadline)

    # Check server-side deadline (with 5-second buffer for network transit)
    if deadline and now > deadline + timedelta(seconds=5):
        finalize_mock_attempt(attempt, status='timed_out')
        return jsonify({
            'status': 'expired',
            'message': 'Time expired. The test has been automatically submitted.',
            'redirect_url': url_for('mock.result', attempt_id=attempt.id)
        }), 200

    if attempt.status != 'in_progress':
        return jsonify({
            'status': 'submitted',
            'message': 'Test has already been submitted.',
            'redirect_url': url_for('mock.result', attempt_id=attempt.id)
        }), 200

    data = request.get_json(silent=True) or {}
    question_id = data.get('question_id')

    if not question_id:
        return jsonify({'error': 'Missing question_id'}), 400

    chosen_option = data.get('chosen_option')
    marked_for_review = bool(data.get('marked_for_review', False))
    time_spent_delta = int(data.get('time_spent', 0))

    # Verify that the question belongs to this test
    question = MockQuestion.query.get(question_id)
    if not question or question.section.test_id != attempt.test_id:
        return jsonify({'error': 'Invalid question for this test'}), 400

    # Sanitize chosen_option: must be None or 1..4
    if chosen_option is not None:
        try:
            chosen_option = int(chosen_option)
            if chosen_option not in (1, 2, 3, 4):
                chosen_option = None
        except (ValueError, TypeError):
            chosen_option = None

    # Update or create answer record
    answer = MockAnswer.query.filter_by(
        attempt_id=attempt.id,
        question_id=question_id
    ).first()

    if not answer:
        answer = MockAnswer(
            attempt_id=attempt.id,
            question_id=question_id,
            chosen_option=chosen_option,
            marked_for_review=marked_for_review,
            time_spent=max(0, time_spent_delta)
        )
        db.session.add(answer)
    else:
        answer.chosen_option = chosen_option
        answer.marked_for_review = marked_for_review
        if time_spent_delta > 0:
            answer.time_spent += time_spent_delta

    db.session.commit()

    remaining_seconds = max(0, int((deadline - now).total_seconds())) if deadline else 0

    return jsonify({
        'status': 'saved',
        'question_id': question_id,
        'chosen_option': chosen_option,
        'marked_for_review': marked_for_review,
        'seconds_remaining': remaining_seconds
    })


@mock_bp.route('/attempt/<int:attempt_id>/violation', methods=['POST'])
@login_required
@limiter.limit("60/minute")
def record_violation(attempt_id):
    """
    Record an anti-cheat discipline event (tab switch, window blur, fullscreen exit).
    Increments server-side violation_count with 1-second debounce.
    Auto-submits on 3rd violation.
    """
    attempt = MockAttempt.query.get_or_404(attempt_id)

    # Security: IDOR verification
    if attempt.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    if not attempt.test.is_active:
        return jsonify({'error': 'This mock test is inactive.'}), 403

    if attempt.status != 'in_progress':
        return jsonify({
            'status': 'already_submitted',
            'redirect_url': url_for('mock.result', attempt_id=attempt.id)
        }), 200

    now = datetime.utcnow()
    deadline = normalize_utc(attempt.server_deadline)

    # Check deadline
    if deadline and now > deadline + timedelta(seconds=5):
        finalize_mock_attempt(attempt, status='timed_out')
        return jsonify({
            'status': 'expired',
            'redirect_url': url_for('mock.result', attempt_id=attempt.id),
            'message': 'Time limit expired! Your test has been submitted automatically.'
        }), 200

    payload = request.get_json(silent=True) or {}
    v_type = payload.get('violation_type', 'tab_switch')
    if v_type not in ('tab_switch', 'window_blur', 'fullscreen_exit'):
        v_type = 'tab_switch'

    # Debounce: check if a violation was recorded within the last 1.0 second
    latest_v = MockViolation.query.filter_by(
        attempt_id=attempt.id
    ).order_by(MockViolation.timestamp.desc()).first()

    if latest_v:
        v_ts = normalize_utc(latest_v.timestamp)
        if v_ts and (now - v_ts).total_seconds() < 1.0:
            return jsonify({
                'status': 'debounced',
                'violation_count': attempt.violation_count,
                'max_violations': 3
            }), 200

    # Log violation record
    violation = MockViolation(
        attempt_id=attempt.id,
        violation_type=v_type,
        timestamp=now
    )
    db.session.add(violation)
    attempt.violation_count += 1

    if attempt.violation_count >= 3:
        finalize_mock_attempt(attempt, status='disqualified')
        db.session.commit()
        logger.warning("Attempt %d for user %s auto-submitted due to 3 discipline violations.",
                       attempt.id, current_user.username)
        return jsonify({
            'status': 'disqualified',
            'violation_count': attempt.violation_count,
            'max_violations': 3,
            'redirect_url': url_for('mock.result', attempt_id=attempt.id),
            'message': 'Maximum discipline warnings (3 of 3) reached. Your assessment has been automatically submitted.'
        }), 200

    db.session.commit()
    logger.info("Violation %d/3 recorded for attempt %d (user: %s, type: %s)",
                attempt.violation_count, attempt.id, current_user.username, v_type)

    return jsonify({
        'status': 'warning',
        'violation_count': attempt.violation_count,
        'max_violations': 3,
        'message': f'Warning {attempt.violation_count} of 3: Loss of window focus, tab switch, or fullscreen exit detected. Please remain on the exam screen.'
    }), 200


@mock_bp.route('/attempt/<int:attempt_id>/submit', methods=['POST'])
@login_required
@limiter.limit("30/minute")
def submit_test(attempt_id):
    """
    Final submission of the exam.
    Computes section and overall score with zero negative marking.
    """
    attempt = MockAttempt.query.get_or_404(attempt_id)

    # IDOR check
    if attempt.user_id != current_user.id:
        abort(403)

    if attempt.status != 'in_progress':
        return redirect(url_for('mock.result', attempt_id=attempt.id))

    status = 'completed'
    deadline = normalize_utc(attempt.server_deadline)
    if deadline and datetime.utcnow() >= deadline + timedelta(seconds=5):
        status = 'timed_out'

    # Rule: All questions are mandatory for manual submission.
    # Timer expiry (timed_out) and 3rd violation (disqualified) bypass this and auto-submit.
    if status != 'timed_out':
        total_questions = sum(len(sec.questions) for sec in attempt.test.sections)
        answered_count = MockAnswer.query.filter(
            MockAnswer.attempt_id == attempt.id,
            MockAnswer.chosen_option.isnot(None)
        ).count()

        if answered_count < total_questions:
            remaining = total_questions - answered_count
            flash(f'Cannot submit: All questions are mandatory. You have {remaining} unanswered question(s) remaining.', 'danger')
            return redirect(url_for('mock.take_test', attempt_id=attempt.id))

    finalize_mock_attempt(attempt, status=status)
    if status == 'timed_out':
        flash('Time elapsed! Your mock test has been automatically submitted.', 'info')
    else:
        flash('Your mock test has been submitted successfully!', 'success')
    return redirect(url_for('mock.result', attempt_id=attempt.id))


@mock_bp.route('/attempt/<int:attempt_id>/result')
@login_required
def result(attempt_id):
    """
    Detailed result page with section-wise scores, accuracy, and explanations.
    """
    attempt = MockAttempt.query.get_or_404(attempt_id)

    # Only student who took the test or admin can view results
    if attempt.user_id != current_user.id and not current_user.is_admin():
        abort(403)

    # Build section-wise performance statistics
    section_stats = []
    answers_map = {a.question_id: a for a in attempt.answers}

    for section in attempt.test.sections:
        sec_total = 0
        sec_score = 0
        sec_answered = 0
        sec_correct = 0
        sec_time = 0
        sec_questions = []

        for q in section.questions:
            sec_total += (q.marks or 1)
            ans = answers_map.get(q.id)

            user_choice = ans.chosen_option if ans else None
            is_correct = (user_choice == q.correct_option) if user_choice is not None else False
            time_spent = ans.time_spent if ans else 0
            sec_time += time_spent

            if user_choice is not None:
                sec_answered += 1
                if is_correct:
                    sec_score += (q.marks or 1)
                    sec_correct += 1

            sec_questions.append({
                'question': q,
                'user_choice': user_choice,
                'is_correct': is_correct,
                'time_spent': time_spent,
                'marked_for_review': ans.marked_for_review if ans else False
            })

        sec_accuracy = round((sec_correct / sec_answered * 100), 1) if sec_answered > 0 else 0.0

        section_stats.append({
            'section': section,
            'total_questions': len(section.questions),
            'total_marks': sec_total,
            'score': sec_score,
            'answered': sec_answered,
            'correct': sec_correct,
            'accuracy': sec_accuracy,
            'time_spent': sec_time,
            'questions_detail': sec_questions
        })

    total_time_spent = sum(s['time_spent'] for s in section_stats)
    overall_accuracy = round(
        (attempt.score / sum(s['answered'] for s in section_stats) * 100), 1
    ) if sum(s['answered'] for s in section_stats) > 0 else 0.0

    return render_template(
        'mock/result.html',
        attempt=attempt,
        test=attempt.test,
        section_stats=section_stats,
        total_time_spent=total_time_spent,
        overall_accuracy=overall_accuracy
    )
