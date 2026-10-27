import unittest
import json
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Role, MockTest, MockSection, MockQuestion, MockAttempt, MockAnswer, MockViolation
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost'


class MockEngineTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Seed Admin and Students
        self.admin = User(username='admin_test', email='admin@test.com', role=Role.ADMIN, is_verified=True)
        self.admin.set_password('AdminPass123')

        self.student1 = User(username='student1', email='student1@test.com', role=Role.USER, is_verified=True)
        self.student1.set_password('StudentPass123')

        self.student2 = User(username='student2', email='student2@test.com', role=Role.USER, is_verified=True)
        self.student2.set_password('StudentPass123')

        db.session.add_all([self.admin, self.student1, self.student2])
        db.session.commit()

        # Seed Sample Mock Test with 2 Sections and Questions
        self.test = MockTest(
            company_name='TCS',
            title='TCS NQT Diagnostic Mock',
            description='Practice test for numerical and verbal ability.',
            duration_minutes=30,
            is_active=True,
            allow_multiple_attempts=False
        )
        db.session.add(self.test)
        db.session.commit()

        self.sec1 = MockSection(test_id=self.test.id, name='Numerical Ability', order=1, num_questions=2)
        self.sec2 = MockSection(test_id=self.test.id, name='Verbal Ability', order=2, num_questions=1)
        db.session.add_all([self.sec1, self.sec2])
        db.session.commit()

        self.q1 = MockQuestion(
            section_id=self.sec1.id,
            text='What is 15 * 14?',
            option1='210', option2='220', option3='200', option4='190',
            correct_option=1, explanation='15 * 14 = 210', marks=1
        )
        self.q2 = MockQuestion(
            section_id=self.sec1.id,
            text='Solve: 2^6 = ?',
            option1='32', option2='64', option3='128', option4='16',
            correct_option=2, explanation='2^6 = 64', marks=1
        )
        self.q3 = MockQuestion(
            section_id=self.sec2.id,
            text='Synonym of "Meticulous":',
            option1='Careless', option2='Rapid', option3='Diligent and precise', option4='Hesitant',
            correct_option=3, explanation='Meticulous means showing great attention to detail.', marks=1
        )
        db.session.add_all([self.q1, self.q2, self.q3])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login_as(self, user):
        from flask import g
        if hasattr(g, '_login_user'):
            delattr(g, '_login_user')
        self.client = self.app.test_client()
        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(user.id)
            sess['_fresh'] = True

    # 1. Admin Model & Management
    def test_01_admin_mock_models_and_counts(self):
        self.assertEqual(self.test.total_questions_count(), 3)
        self.assertEqual(self.test.total_marks(), 3)
        self.assertEqual(len(self.test.sections), 2)

    # 2. Student Start Test & Server-Side Deadline
    def test_02_student_start_test_creates_server_deadline(self):
        self.login_as(self.student1)
        resp = self.client.post(f'/mock/test/{self.test.id}/start', follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()
        self.assertIsNotNone(attempt)
        self.assertEqual(attempt.status, 'in_progress')
        self.assertIsNotNone(attempt.started_at)
        self.assertIsNotNone(attempt.server_deadline)

        # Server deadline must be approx started_at + 30 minutes
        expected_deadline = attempt.started_at + timedelta(minutes=30)
        diff_seconds = abs((attempt.server_deadline - expected_deadline).total_seconds())
        self.assertLess(diff_seconds, 2)

    # 3. Per-Student Shuffling Persistence
    def test_03_shuffling_stored_in_attempt_persists_across_refreshes(self):
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')

        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()
        self.assertIsNotNone(attempt.question_order)
        initial_order = json.dumps(attempt.question_order, sort_keys=True)

        # Access take_test route (simulating refresh)
        resp = self.client.get(f'/mock/attempt/{attempt.id}')
        self.assertEqual(resp.status_code, 200)

        # Re-fetch attempt from DB; order must be identical
        attempt_after = MockAttempt.query.get(attempt.id)
        self.assertEqual(json.dumps(attempt_after.question_order, sort_keys=True), initial_order)

    # 4. Single Attempt Rule & Retake Toggle
    def test_04_single_attempt_rule(self):
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()

        # Answer all questions so manual submit is permitted
        for q in [self.q1, self.q2, self.q3]:
            self.client.post(
                f'/mock/attempt/{attempt.id}/save',
                data=json.dumps({'question_id': q.id, 'chosen_option': 1, 'time_spent': 5}),
                content_type='application/json'
            )

        # Submit the attempt
        self.client.post(f'/mock/attempt/{attempt.id}/submit')
        db.session.refresh(attempt)
        self.assertEqual(attempt.status, 'completed')

        # Try starting a second attempt when allow_multiple_attempts is False
        resp = self.client.post(f'/mock/test/{self.test.id}/start', follow_redirects=False)
        self.assertEqual(resp.status_code, 302)
        self.assertIn(f'/mock/attempt/{attempt.id}/result', resp.location)

        # Total attempts for student1 must still be exactly 1
        attempts_count = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).count()
        self.assertEqual(attempts_count, 1)

    # 5. Configurable Multiple Attempts
    def test_05_multiple_attempts_allowed_when_enabled(self):
        self.test.allow_multiple_attempts = True
        db.session.commit()

        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt1 = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()

        # Answer all questions so manual submit is permitted
        for q in [self.q1, self.q2, self.q3]:
            self.client.post(
                f'/mock/attempt/{attempt1.id}/save',
                data=json.dumps({'question_id': q.id, 'chosen_option': 1, 'time_spent': 5}),
                content_type='application/json'
            )
        self.client.post(f'/mock/attempt/{attempt1.id}/submit')

        # Start second attempt
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempts = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).all()
        self.assertEqual(len(attempts), 2)

    # 6. AJAX Autosave & IDOR Protection
    def test_06_ajax_autosave_and_idor_protection(self):
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()

        # Student1 autosaves answer
        payload = {
            'question_id': self.q1.id,
            'chosen_option': 1,
            'marked_for_review': True,
            'time_spent': 20
        }
        resp = self.client.post(
            f'/mock/attempt/{attempt.id}/save',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data['status'], 'saved')
        self.assertEqual(data['chosen_option'], 1)
        self.assertTrue(data['marked_for_review'])

        # Verify in DB
        ans = MockAnswer.query.filter_by(attempt_id=attempt.id, question_id=self.q1.id).first()
        self.assertIsNotNone(ans)
        self.assertEqual(ans.chosen_option, 1)
        self.assertTrue(ans.marked_for_review)
        self.assertEqual(ans.time_spent, 20)

        # IDOR Test: Student2 tries to save answer to Student1's attempt
        self.login_as(self.student2)
        resp2 = self.client.post(
            f'/mock/attempt/{attempt.id}/save',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp2.status_code, 403)

    # 7. Server-Side Deadline Expiration & Auto-Submission
    def test_07_server_deadline_expired_autosubmits(self):
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()

        # Simulate deadline elapsed in the past
        attempt.server_deadline = datetime.utcnow() - timedelta(minutes=5)
        db.session.commit()

        # Attempt to save an answer after deadline
        payload = {'question_id': self.q1.id, 'chosen_option': 1, 'time_spent': 5}
        resp = self.client.post(
            f'/mock/attempt/{attempt.id}/save',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data['status'], 'expired')
        self.assertIn(f'/mock/attempt/{attempt.id}/result', data['redirect_url'])

        # Verify attempt status became 'timed_out'
        db.session.refresh(attempt)
        self.assertEqual(attempt.status, 'timed_out')
        self.assertIsNotNone(attempt.submitted_at)

    # 8. Score Calculation: Zero Negative Marking
    def test_08_zero_negative_marking_calculation(self):
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()

        # Answer Q1 correctly (correct_option=1) -> +1
        self.client.post(
            f'/mock/attempt/{attempt.id}/save',
            data=json.dumps({'question_id': self.q1.id, 'chosen_option': 1, 'time_spent': 10}),
            content_type='application/json'
        )

        # Answer Q2 incorrectly (correct_option=2, student chooses 3) -> 0 pts (NO negative marking)
        self.client.post(
            f'/mock/attempt/{attempt.id}/save',
            data=json.dumps({'question_id': self.q2.id, 'chosen_option': 3, 'time_spent': 15}),
            content_type='application/json'
        )

        # Answer Q3 incorrectly (correct_option=1, student chooses 4) -> 0 pts (NO negative marking)
        self.client.post(
            f'/mock/attempt/{attempt.id}/save',
            data=json.dumps({'question_id': self.q3.id, 'chosen_option': 4, 'time_spent': 5}),
            content_type='application/json'
        )

        # Submit test
        self.client.post(f'/mock/attempt/{attempt.id}/submit')
        db.session.refresh(attempt)

        self.assertEqual(attempt.status, 'completed')
        self.assertEqual(attempt.score, 1)       # 1 correct out of 3
        self.assertEqual(attempt.total_marks, 3) # Total 3 marks
        self.assertGreaterEqual(attempt.score, 0) # Zero negative marking strictly honored

    # 9. Security & Anti-Cheat: Exam Page & AJAX Autosave NEVER Leak Correct Answers or Explanations
    def test_09_exam_page_and_save_never_leak_correct_option_or_explanation(self):
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()

        # Fetch Exam Page HTML
        resp = self.client.get(f'/mock/attempt/{attempt.id}')
        self.assertEqual(resp.status_code, 200)
        html_content = resp.get_data(as_text=True)

        # Confirm questions are rendered
        self.assertIn("What is 15 * 14?", html_content)

        # CONFIRM: correct_option is NOT present anywhere in the HTML/JS
        self.assertNotIn('correct_option', html_content)

        # CONFIRM: question explanations are NOT present anywhere in the HTML/JS
        self.assertNotIn('15 * 14 = 210', html_content)
        self.assertNotIn('Meticulous means showing great attention to detail.', html_content)
        self.assertNotIn('2^6 = 64', html_content)

        # Autosave response check: must never leak correct_option or explanation
        save_resp = self.client.post(
            f'/mock/attempt/{attempt.id}/save',
            data=json.dumps({'question_id': self.q1.id, 'chosen_option': 1, 'time_spent': 5}),
            content_type='application/json'
        )
        self.assertEqual(save_resp.status_code, 200)
        save_json = save_resp.get_json()
        self.assertNotIn('correct_option', save_json)
        self.assertNotIn('explanation', save_json)
        self.assertNotIn('is_correct', save_json)

    # 10. Inactive Test Cannot Be Opened or Started by URL
    def test_10_inactive_test_cannot_be_opened_or_started(self):
        # Create an inactive test
        inactive_test = MockTest(
            company_name='Infosys',
            title='Infosys Mock (Inactive)',
            duration_minutes=45,
            is_active=False
        )
        db.session.add(inactive_test)
        db.session.commit()

        self.login_as(self.student1)

        # 1. Accessing instructions directly -> redirected with warning
        resp1 = self.client.get(f'/mock/test/{inactive_test.id}/instructions')
        self.assertEqual(resp1.status_code, 302)
        self.assertIn('/mock/tests', resp1.headers.get('Location', ''))

        # 2. Starting inactive test -> rejected
        resp2 = self.client.post(f'/mock/test/{inactive_test.id}/start')
        self.assertEqual(resp2.status_code, 302)
        self.assertIn('/mock/tests', resp2.headers.get('Location', ''))

        # 3. Direct attempt URL for deactivated test -> rejected
        attempt = MockAttempt(
            user_id=self.student1.id,
            test_id=inactive_test.id,
            started_at=datetime.utcnow(),
            server_deadline=datetime.utcnow() + timedelta(minutes=45),
            status='in_progress',
            question_order={'sections': []}
        )
        db.session.add(attempt)
        db.session.commit()

        resp3 = self.client.get(f'/mock/attempt/{attempt.id}')
        self.assertEqual(resp3.status_code, 302)
        self.assertIn('/mock/tests', resp3.headers.get('Location', ''))

        # 4. Autosave to inactive test -> 403
        resp4 = self.client.post(
            f'/mock/attempt/{attempt.id}/save',
            data=json.dumps({'question_id': self.q1.id, 'chosen_option': 1, 'time_spent': 5}),
            content_type='application/json'
        )
        self.assertEqual(resp4.status_code, 403)

    # 11. Admin Mock Routes Strictly Require Admin Role
    def test_11_admin_mock_routes_require_admin_role(self):
        # Student tries to access admin mock pages
        self.login_as(self.student1)

        admin_urls = [
            '/admin/mock-tests',
            '/admin/mock-tests/new',
            f'/admin/mock-tests/{self.test.id}/edit',
            f'/admin/mock-tests/{self.test.id}/sections',
            f'/admin/mock-tests/sections/{self.sec1.id}/questions',
            f'/admin/mock-tests/sections/{self.sec1.id}/questions/new',
            f'/admin/mock-tests/sections/{self.sec1.id}/bulk-add',
        ]
        for url in admin_urls:
            resp = self.client.get(url)
            # admin_required redirects non-admins (302)
            self.assertEqual(resp.status_code, 302, f"Failed for {url}")

    # 12. Question Form & Bulk Add Strictly Validate Correct Option 1-4
    def test_12_question_validation_rejects_invalid_correct_option(self):
        self.login_as(self.admin)

        # Invalid correct_option (5)
        resp1 = self.client.post(
            f'/admin/mock-tests/sections/{self.sec1.id}/questions/new',
            data={
                'text': 'Invalid question',
                'option1': 'A',
                'option2': 'B',
                'correct_option': '5',
                'marks': '1'
            },
            follow_redirects=True
        )
        self.assertIn('Correct Option must be between 1 and 4', resp1.get_data(as_text=True))

        # Bulk add with invalid row
        resp2 = self.client.post(
            f'/admin/mock-tests/sections/{self.sec1.id}/bulk-add',
            data={
                'num_questions': '1',
                'text_1': 'Bulk Q1',
                'option1_1': 'A',
                'option2_1': 'B',
                'correct_option_1': '9',
                'marks_1': '1'
            },
            follow_redirects=True
        )
        self.assertIn('Correct Option must be between 1 and 4', resp2.get_data(as_text=True))

    # 13. Phase C: Violation Increments Server-Side and Persists Across Refresh
    def test_13_violation_increments_server_side_and_persists_across_refresh(self):
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()
        self.assertEqual(attempt.violation_count, 0)

        # Trigger first violation: tab_switch
        resp1 = self.client.post(
            f'/mock/attempt/{attempt.id}/violation',
            data=json.dumps({'violation_type': 'tab_switch'}),
            content_type='application/json'
        )
        self.assertEqual(resp1.status_code, 200)
        data1 = resp1.get_json()
        self.assertEqual(data1['status'], 'warning')
        self.assertEqual(data1['violation_count'], 1)

        db.session.refresh(attempt)
        self.assertEqual(attempt.violation_count, 1)
        self.assertEqual(len(attempt.violations), 1)
        self.assertEqual(attempt.violations[0].violation_type, 'tab_switch')

        # Refresh page (client cannot reset server violation count)
        refresh_resp = self.client.get(f'/mock/attempt/{attempt.id}')
        self.assertEqual(refresh_resp.status_code, 200)
        db.session.refresh(attempt)
        self.assertEqual(attempt.violation_count, 1)

    # 14. Phase C: 3rd Violation Auto-Submits and Marks Disqualified
    def test_14_third_violation_triggers_auto_submission_and_disqualification(self):
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()

        # Violation 1 (tab_switch)
        resp1 = self.client.post(
            f'/mock/attempt/{attempt.id}/violation',
            data=json.dumps({'violation_type': 'tab_switch'}),
            content_type='application/json'
        )
        self.assertEqual(resp1.get_json()['status'], 'warning')
        self.assertEqual(resp1.get_json()['violation_count'], 1)

        # Fast forward time beyond 1s debounce
        v1 = MockViolation.query.filter_by(attempt_id=attempt.id).order_by(MockViolation.timestamp.desc()).first()
        v1.timestamp = datetime.utcnow() - timedelta(seconds=2)
        db.session.commit()

        # Violation 2 (window_blur)
        resp2 = self.client.post(
            f'/mock/attempt/{attempt.id}/violation',
            data=json.dumps({'violation_type': 'window_blur'}),
            content_type='application/json'
        )
        self.assertEqual(resp2.get_json()['status'], 'warning')
        self.assertEqual(resp2.get_json()['violation_count'], 2)

        # Fast forward time beyond 1s debounce
        v2 = MockViolation.query.filter_by(attempt_id=attempt.id).order_by(MockViolation.timestamp.desc()).first()
        v2.timestamp = datetime.utcnow() - timedelta(seconds=2)
        db.session.commit()

        # Violation 3 (fullscreen_exit) -> Triggers auto-submit
        resp3 = self.client.post(
            f'/mock/attempt/{attempt.id}/violation',
            data=json.dumps({'violation_type': 'fullscreen_exit'}),
            content_type='application/json'
        )
        data3 = resp3.get_json()
        self.assertEqual(data3['status'], 'disqualified')
        self.assertEqual(data3['violation_count'], 3)
        self.assertIn(f'/mock/attempt/{attempt.id}/result', data3['redirect_url'])

        # Verify in database: status is disqualified and submitted_at is set
        db.session.refresh(attempt)
        self.assertEqual(attempt.status, 'disqualified')
        self.assertEqual(attempt.violation_count, 3)
        self.assertIsNotNone(attempt.submitted_at)

    # 15. Phase C: IDOR Protection on Violation Endpoint
    def test_15_idor_protection_blocks_posting_violations_to_another_users_attempt(self):
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()

        # Student2 tries to trigger a violation on Student1's attempt
        self.login_as(self.student2)
        resp = self.client.post(
            f'/mock/attempt/{attempt.id}/violation',
            data=json.dumps({'violation_type': 'tab_switch'}),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 403)

        # Verify Student1's count is still 0
        db.session.refresh(attempt)
        self.assertEqual(attempt.violation_count, 0)

    # 16. Phase C: Duplicate Violation Events within 1 Second Are Debounced
    def test_16_duplicate_violation_events_within_one_second_debounced(self):
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()

        # First violation event (e.g. visibilitychange)
        resp1 = self.client.post(
            f'/mock/attempt/{attempt.id}/violation',
            data=json.dumps({'violation_type': 'tab_switch'}),
            content_type='application/json'
        )
        self.assertEqual(resp1.get_json()['status'], 'warning')
        self.assertEqual(resp1.get_json()['violation_count'], 1)

        # Second violation event fired immediately within milliseconds (e.g. blur companion event)
        resp2 = self.client.post(
            f'/mock/attempt/{attempt.id}/violation',
            data=json.dumps({'violation_type': 'window_blur'}),
            content_type='application/json'
        )
        self.assertEqual(resp2.get_json()['status'], 'debounced')
        self.assertEqual(resp2.get_json()['violation_count'], 1)

        # Verify DB still has exactly 1 violation
        db.session.refresh(attempt)
        self.assertEqual(attempt.violation_count, 1)
        self.assertEqual(len(attempt.violations), 1)

    # 17. Phase D: Manual Submit Blocked When Questions Are Unanswered
    def test_17_manual_submit_blocked_when_questions_unanswered(self):
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()

        # Answer only 1 of 3 questions
        self.client.post(
            f'/mock/attempt/{attempt.id}/save',
            data=json.dumps({'question_id': self.q1.id, 'chosen_option': 1, 'time_spent': 10}),
            content_type='application/json'
        )

        # Attempt manual submission
        resp = self.client.post(f'/mock/attempt/{attempt.id}/submit', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertIn('Cannot submit: All questions are mandatory', html)
        self.assertIn('2 unanswered question(s) remaining', html)

        # Attempt remains in progress
        db.session.refresh(attempt)
        self.assertEqual(attempt.status, 'in_progress')
        self.assertIsNone(attempt.submitted_at)

    # 18. Phase D: Manual Submit Succeeds When All Questions Are Answered
    def test_18_manual_submit_succeeds_when_all_questions_answered(self):
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()

        # Answer all 3 questions
        for q, opt in [(self.q1, 1), (self.q2, 2), (self.q3, 1)]:
            self.client.post(
                f'/mock/attempt/{attempt.id}/save',
                data=json.dumps({'question_id': q.id, 'chosen_option': opt, 'time_spent': 5}),
                content_type='application/json'
            )

        resp = self.client.post(f'/mock/attempt/{attempt.id}/submit', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertIn('Your mock test has been submitted successfully', html)
        db.session.refresh(attempt)
        self.assertEqual(attempt.status, 'completed')
        self.assertIsNotNone(attempt.submitted_at)

    # 19. Phase D: Timer Expiry and 3rd Violation Still Auto-Submit with Partial Answers
    def test_19_timer_expiry_and_violation_auto_submit_with_partial_answers(self):
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()

        # Answer only Q1 correctly (+1), leave Q2 and Q3 unanswered
        self.client.post(
            f'/mock/attempt/{attempt.id}/save',
            data=json.dumps({'question_id': self.q1.id, 'chosen_option': 1, 'time_spent': 5}),
            content_type='application/json'
        )

        # Simulate deadline elapsed
        attempt.server_deadline = datetime.utcnow() - timedelta(seconds=10)
        db.session.commit()

        # Post submit (triggering timeout auto-finalization)
        resp = self.client.post(f'/mock/attempt/{attempt.id}/submit', follow_redirects=True)
        html = resp.get_data(as_text=True)

        db.session.refresh(attempt)
        self.assertEqual(attempt.status, 'timed_out')
        self.assertEqual(attempt.score, 1)  # 1 mark for Q1, 0 for unanswered
        self.assertEqual(attempt.total_marks, 3)
        self.assertIn('Auto-submitted when time ended', html)

    # 20. Phase D: Begin Exam Overlay Rendered and Gated
    def test_20_begin_exam_overlay_and_submit_disabled_rendered(self):
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()

        resp = self.client.get(f'/mock/attempt/{attempt.id}')
        html = resp.get_data(as_text=True)

        self.assertIn('id="beginExamOverlay"', html)
        self.assertIn('id="beginExamBtn"', html)
        self.assertIn('id="submitExamBtn"', html)
        self.assertIn('disabled', html)

    # 21. Phase D: Admin Reset Attempt Flow Lets Student Retake Test
    def test_21_admin_reset_attempt_flow(self):
        # 1. Student completes test
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()

        # Answer all and submit
        for q in [self.q1, self.q2, self.q3]:
            self.client.post(
                f'/mock/attempt/{attempt.id}/save',
                data=json.dumps({'question_id': q.id, 'chosen_option': 1, 'time_spent': 5}),
                content_type='application/json'
            )
        self.client.post(f'/mock/attempt/{attempt.id}/submit')
        db.session.refresh(attempt)
        self.assertEqual(attempt.status, 'completed')

        # Student is blocked from starting another attempt
        re_resp = self.client.get(f'/mock/test/{self.test.id}/instructions', follow_redirects=True)
        self.assertIn('Viewing your results', re_resp.get_data(as_text=True))

        # 2. Admin inspects attempts list
        self.login_as(self.admin)
        att_resp = self.client.get(f'/admin/mock-tests/{self.test.id}/attempts')
        self.assertEqual(att_resp.status_code, 200)
        self.assertIn(self.student1.username, att_resp.get_data(as_text=True))

        # 3. Admin resets attempt
        reset_resp = self.client.post(f'/admin/mock-attempts/{attempt.id}/reset', follow_redirects=True)
        self.assertEqual(reset_resp.status_code, 200)
        self.assertIn('was reset successfully', reset_resp.get_data(as_text=True))

        # Verify attempt was deleted from database
        deleted_att = MockAttempt.query.get(attempt.id)
        self.assertIsNone(deleted_att)

        # 4. Student can now retake the test!
        self.login_as(self.student1)
        instructions_resp = self.client.get(f'/mock/test/{self.test.id}/instructions')
        self.assertEqual(instructions_resp.status_code, 200)
        self.assertIn('I am Ready to Begin', instructions_resp.get_data(as_text=True))

    # 22. Phase D: Placement Mocks Listing Groups by Company and Hides Inactive Tests
    def test_22_placement_mocks_catalog_groups_by_company_and_hides_inactive(self):
        # Create an inactive test
        inactive_test = MockTest(
            company_name='Wipro',
            title='Wipro Draft Assessment',
            duration_minutes=60,
            is_active=False
        )
        db.session.add(inactive_test)
        db.session.commit()

        self.login_as(self.student1)
        resp = self.client.get('/mock/tests')
        html = resp.get_data(as_text=True)

        self.assertIn(self.test.company_name, html)
        self.assertIn(self.test.title, html)
        self.assertNotIn('Wipro Draft Assessment', html)

    # 23. Regression: Timezone-aware server_deadline (PostgreSQL) & string question_order handling
    def test_23_timezone_aware_and_json_string_compatibility(self):
        from datetime import timezone
        self.login_as(self.student1)
        self.client.post(f'/mock/test/{self.test.id}/start')
        attempt = MockAttempt.query.filter_by(user_id=self.student1.id, test_id=self.test.id).first()

        # Simulate PostgreSQL psycopg2 timezone-aware datetime
        attempt.server_deadline = datetime.now(timezone.utc) + timedelta(minutes=30)
        # Simulate JSON serialized as raw string in database
        import json
        attempt.question_order = json.dumps(attempt.question_order)
        db.session.commit()

        # Attempt page MUST load smoothly without TypeError or AttributeError
        resp = self.client.get(f'/mock/attempt/{attempt.id}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.test.title, resp.get_data(as_text=True))

        # Autosave MUST succeed
        q1 = self.sec1.questions[0]
        save_resp = self.client.post(
            f'/mock/attempt/{attempt.id}/save',
            json={'question_id': q1.id, 'chosen_option': 1, 'time_spent': 5}
        )
        self.assertEqual(save_resp.status_code, 200)
        self.assertEqual(save_resp.get_json()['status'], 'saved')

        # Violation debounce with aware violation timestamp MUST succeed
        v_aware = MockViolation(
            attempt_id=attempt.id,
            violation_type='tab_switch',
            timestamp=datetime.now(timezone.utc)
        )
        db.session.add(v_aware)
        db.session.commit()

        viol_resp = self.client.post(
            f'/mock/attempt/{attempt.id}/violation',
            json={'violation_type': 'window_blur'}
        )
        self.assertEqual(viol_resp.status_code, 200)
        self.assertEqual(viol_resp.get_json()['status'], 'debounced')


if __name__ == '__main__':
    unittest.main()


