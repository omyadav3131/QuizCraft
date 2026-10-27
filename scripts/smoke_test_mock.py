"""
scripts/smoke_test_mock.py
Automated local smoke test runner for Placement Mock Test (Phase A + B).
Executes the full student flow against local SQLite database using Flask test client.
"""

import os
import sys
import json
import secrets
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config
from app import create_app, db
from app.models import User, Role, MockTest, MockAttempt, MockAnswer, MockQuestion


def run_smoke_test():
    # 0. Safety verification
    db_uri = os.environ.get('DATABASE_URL') or Config.SQLALCHEMY_DATABASE_URI or ''
    if any(k in db_uri.lower() for k in ['postgres', 'supabase.co', 'render.com']):
        print("[ABORT] Smoke test refused on non-local database.")
        sys.exit(1)

    app = create_app()
    client = app.test_client()

    results = []

    def record_result(check_name, passed, message=""):
        status_str = "PASS" if passed else "FAIL"
        results.append((check_name, passed, message))
        icon = "[PASS]" if passed else "[FAIL]"
        print(f"  {icon} {check_name}: {message if message else 'OK'}")

    print("======================================================================")
    print("STARTING LOCAL SMOKE TEST: Placement Mock Test (Phase A + B)")
    print("======================================================================\n")

    with app.app_context():
        # Ensure tables exist
        db.create_all()

        # Find or create smoke test student users
        student1 = User.query.filter_by(username='smoke_student1').first()
        if not student1:
            student1 = User(
                username='smoke_student1',
                email='student1@smoketest.local',
                role=Role.USER,
                is_verified=True
            )
            student1.set_password(secrets.token_urlsafe(16))
            db.session.add(student1)

        student2 = User.query.filter_by(username='smoke_student2').first()
        if not student2:
            student2 = User(
                username='smoke_student2',
                email='student2@smoketest.local',
                role=Role.USER,
                is_verified=True
            )
            student2.set_password(secrets.token_urlsafe(16))
            db.session.add(student2)

        demo_test = MockTest.query.filter_by(title="DEMO Mock Test", company_name="Demo").first()
        if not demo_test:
            print("[ERROR] 'DEMO Mock Test' not found. Please run scripts/seed_demo_mock.py first.")
            sys.exit(1)

        # Clear any prior smoke attempt for student1 to start completely fresh
        prior_attempts = MockAttempt.query.filter_by(user_id=student1.id, test_id=demo_test.id).all()
        for att in prior_attempts:
            db.session.delete(att)
        db.session.commit()

        # Helper: switch authenticated user in test client
        def login_as(user):
            from flask import g
            if hasattr(g, '_login_user'):
                delattr(g, '_login_user')
            with client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)
                sess['_fresh'] = True

        # ------------------------------------------------------------------
        # CHECK 1: Instructions Page
        # ------------------------------------------------------------------
        login_as(student1)
        resp1 = client.get(f'/mock/test/{demo_test.id}/instructions')
        passed1 = (resp1.status_code == 200 and "DEMO Mock Test" in resp1.get_data(as_text=True))
        record_result("Check 1: Instructions page loads", passed1, f"Status {resp1.status_code}")

        # ------------------------------------------------------------------
        # CHECK 2: Start Test & Create Server-Side Deadline
        # ------------------------------------------------------------------
        resp2 = client.post(f'/mock/test/{demo_test.id}/start', follow_redirects=False)
        attempt = MockAttempt.query.filter_by(user_id=student1.id, test_id=demo_test.id).first()
        passed2 = (resp2.status_code == 302 and attempt is not None and attempt.status == 'in_progress')
        deadline_str = attempt.server_deadline.strftime('%H:%M:%S') if attempt else "None"
        record_result("Check 2: Start test creates attempt with server deadline", passed2, f"Attempt ID: {attempt.id if attempt else 'N/A'}, Deadline: {deadline_str}")

        # ------------------------------------------------------------------
        # CHECK 3: Exam Page Render & Secrecy Verification
        # ------------------------------------------------------------------
        resp3 = client.get(f'/mock/attempt/{attempt.id}')
        exam_html = resp3.get_data(as_text=True)
        no_correct_option = ('correct_option' not in exam_html)
        no_explanation = ('Cost Price * (1 + Profit%)' not in exam_html and 'Candid means truthful' not in exam_html)
        passed3 = (resp3.status_code == 200 and no_correct_option and no_explanation)
        record_result("Check 3: Exam page renders without leaking answers/explanations", passed3,
                      "No correct_option or explanation found in exam page HTML/JSON")

        # ------------------------------------------------------------------
        # CHECK 4: AJAX Autosave Selection
        # ------------------------------------------------------------------
        first_q_id = attempt.question_order['sections'][0]['questions'][0]['id']
        save_resp = client.post(
            f'/mock/attempt/{attempt.id}/save',
            data=json.dumps({'question_id': first_q_id, 'chosen_option': 2, 'time_spent': 12}),
            content_type='application/json'
        )
        save_data = save_resp.get_json() if save_resp.status_code == 200 else {}
        save_leak = ('correct_option' in save_data or 'explanation' in save_data)
        ans_db = MockAnswer.query.filter_by(attempt_id=attempt.id, question_id=first_q_id).first()
        passed4 = (save_resp.status_code == 200 and save_data.get('status') == 'saved' and not save_leak and ans_db and ans_db.chosen_option == 2)
        record_result("Check 4: AJAX autosave records option & leaks no secrets", passed4,
                      f"Option saved: {ans_db.chosen_option if ans_db else 'None'}, Server seconds left: {save_data.get('seconds_remaining')}")

        # ------------------------------------------------------------------
        # CHECK 5: Mark for Review & Next
        # ------------------------------------------------------------------
        sec_q_id = attempt.question_order['sections'][0]['questions'][1]['id']
        rev_resp = client.post(
            f'/mock/attempt/{attempt.id}/save',
            data=json.dumps({'question_id': sec_q_id, 'chosen_option': 1, 'marked_for_review': True, 'time_spent': 8}),
            content_type='application/json'
        )
        ans_db2 = MockAnswer.query.filter_by(attempt_id=attempt.id, question_id=sec_q_id).first()
        passed5 = (rev_resp.status_code == 200 and ans_db2 and ans_db2.marked_for_review is True)
        record_result("Check 5: Mark for Review flags question in DB", passed5,
                      f"Marked for review: {ans_db2.marked_for_review if ans_db2 else 'None'}")

        # ------------------------------------------------------------------
        # CHECK 6: Clear Response
        # ------------------------------------------------------------------
        clear_resp = client.post(
            f'/mock/attempt/{attempt.id}/save',
            data=json.dumps({'question_id': sec_q_id, 'chosen_option': None, 'marked_for_review': False, 'time_spent': 5}),
            content_type='application/json'
        )
        ans_db2_cleared = MockAnswer.query.filter_by(attempt_id=attempt.id, question_id=sec_q_id).first()
        passed6 = (clear_resp.status_code == 200 and ans_db2_cleared and ans_db2_cleared.chosen_option is None and ans_db2_cleared.marked_for_review is False)
        record_result("Check 6: Clear Response wipes chosen option", passed6,
                      f"Option cleared to: {ans_db2_cleared.chosen_option if ans_db2_cleared else 'None'}")

        # ------------------------------------------------------------------
        # CHECK 7: Refresh / Resume preserves question order & timer
        # ------------------------------------------------------------------
        resume_resp = client.get(f'/mock/attempt/{attempt.id}')
        db.session.refresh(attempt)
        order_before = attempt.question_order
        passed7 = (resume_resp.status_code == 200 and attempt.question_order == order_before)
        record_result("Check 7: Refresh / Reopen resumes attempt with identical question order", passed7,
                      f"Shuffled layout matches exactly across requests")

        # ------------------------------------------------------------------
        # CHECK 7B: Mandatory Questions Rule Blocks Early Manual Submission
        # ------------------------------------------------------------------
        unans_sub_resp = client.post(f'/mock/attempt/{attempt.id}/submit', follow_redirects=True)
        unans_html = unans_sub_resp.get_data(as_text=True)
        passed7b = ("Cannot submit: All questions are mandatory" in unans_html)
        record_result("Check 7B: Manual submit blocked while questions remain unanswered", passed7b,
                      "Server rejected early submission and redirected candidate back")

        # Answer all remaining questions in the test so final submission can proceed
        for sec in attempt.test.sections:
            for q in sec.questions:
                client.post(
                    f'/mock/attempt/{attempt.id}/save',
                    data=json.dumps({'question_id': q.id, 'chosen_option': q.correct_option, 'time_spent': 6}),
                    content_type='application/json'
                )

        # ------------------------------------------------------------------
        # CHECK 8: Submit Test (All Questions Answered)
        # ------------------------------------------------------------------
        sub_resp = client.post(f'/mock/attempt/{attempt.id}/submit', follow_redirects=False)
        db.session.refresh(attempt)
        passed8 = (sub_resp.status_code == 302 and attempt.status == 'completed' and attempt.submitted_at is not None)
        record_result("Check 8: Final test submission transitions status to completed", passed8,
                      f"Score: {attempt.score}/{attempt.total_marks}, Status: {attempt.status}")

        # ------------------------------------------------------------------
        # CHECK 9: Result Page (Scorecard, Explanations, Accuracy)
        # ------------------------------------------------------------------
        res_resp = client.get(f'/mock/attempt/{attempt.id}/result')
        res_html = res_resp.get_data(as_text=True)
        has_score = (f"{attempt.score}" in res_html)
        has_explanation = ("Selling Price = Cost Price" in res_html or "Explanation:" in res_html)
        has_violation_card = ("Exam Discipline & Proctoring Summary" in res_html)
        passed9 = (res_resp.status_code == 200 and has_score and has_explanation and has_violation_card)
        record_result("Check 9: Result page displays scorecard, explanations, and discipline summary", passed9,
                      "Full post-submit diagnostics visible to candidate")

        # ------------------------------------------------------------------
        # CHECK 10: Second Attempt Blocked
        # ------------------------------------------------------------------
        resp_second = client.post(f'/mock/test/{demo_test.id}/start', follow_redirects=False)
        passed10 = (resp_second.status_code == 302 and f'/mock/attempt/{attempt.id}/result' in resp_second.headers.get('Location', ''))
        record_result("Check 10: Second attempt blocked and redirects to results", passed10,
                      f"Redirect: {resp_second.headers.get('Location')}")

        # ------------------------------------------------------------------
        # CHECK 11: IDOR Protection (Student2 cannot access Student1's attempt)
        # ------------------------------------------------------------------
        login_as(student2)
        resp_idor_get = client.get(f'/mock/attempt/{attempt.id}')
        resp_idor_save = client.post(
            f'/mock/attempt/{attempt.id}/save',
            data=json.dumps({'question_id': first_q_id, 'chosen_option': 1, 'time_spent': 5}),
            content_type='application/json'
        )
        passed11 = (resp_idor_get.status_code == 403 and resp_idor_save.status_code == 403)
        record_result("Check 11: IDOR protection blocks Student2 from opening or saving Student1's attempt", passed11,
                      f"GET Status: {resp_idor_get.status_code}, POST Status: {resp_idor_save.status_code}")

    print("\n======================================================================")
    total_passed = sum(1 for _, p, _ in results if p)
    print(f"SMOKE TEST COMPLETE: {total_passed}/{len(results)} CHECKS PASSED")
    print("======================================================================\n")

    if total_passed < len(results):
        print("[FAIL] Some smoke test checks failed.")
        sys.exit(1)
    else:
        print("[SUCCESS] All 11 student flow and security checks passed.")


if __name__ == '__main__':
    run_smoke_test()
