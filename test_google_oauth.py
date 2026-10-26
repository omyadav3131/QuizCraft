"""
QuizCraft Phase 2: Google OAuth 2.0 Test Suite
Tests all requirements:
1. Google redirect & CSRF state generation
2. Error response & user cancellation
3. Bad or missing state (CSRF)
4. Unverified Google email rejected
5. First-time Google user registration (password_hash=None, is_verified=True, unique username)
6. Existing user account linking (by verified email, without duplicates)
7. Existing google_id login
8. Admin block (admin cannot login via Google)
9. Google-only user on forgot password
10. Google-only user on change password
11. Google-only user on regular username/password login
"""

import unittest
from unittest.mock import patch, MagicMock
from app import create_app, db
from app.models import User
from config import Config


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    GOOGLE_CLIENT_ID = 'mock-google-client-id.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = 'mock-google-client-secret'
    SERVER_NAME = 'localhost:5000'


class GoogleOAuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_01_google_login_redirect(self):
        """Test /auth/google redirects to Google Auth endpoint with state and client_id."""
        response = self.client.get('/auth/google')
        self.assertEqual(response.status_code, 302)
        location = response.headers.get('Location', '')
        self.assertTrue(location.startswith('https://accounts.google.com/o/oauth2/v2/auth'))
        self.assertIn('client_id=mock-google-client-id', location)
        self.assertIn('response_type=code', location)
        self.assertIn('scope=openid+email+profile', location)
        self.assertIn('state=', location)

        # Confirm state is stored in session
        with self.client.session_transaction() as sess:
            self.assertIn('google_oauth_state', sess)
            self.assertTrue(len(sess['google_oauth_state']) >= 32)

    def test_02_google_callback_user_cancelled(self):
        """Test user cancellation/access_denied handled gracefully with redirect to login."""
        with self.client.session_transaction() as sess:
            sess['google_oauth_state'] = 'test-state-abc'

        response = self.client.get('/auth/google/callback?error=access_denied', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        content = response.get_data(as_text=True)
        self.assertIn('Google Sign-In was cancelled or denied', content)

    def test_03_google_callback_bad_state(self):
        """Test mismatched or missing state fails CSRF verification and redirects to login."""
        with self.client.session_transaction() as sess:
            sess['google_oauth_state'] = 'expected-state-123'

        response = self.client.get('/auth/google/callback?state=wrong-state-456&code=sample_code', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        content = response.get_data(as_text=True)
        self.assertIn('Invalid or expired authentication session', content)

    @patch('requests.post')
    @patch('requests.get')
    def test_04_google_callback_unverified_email_rejected(self, mock_get, mock_post):
        """Test that Google accounts with email_verified=False are strictly rejected."""
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {'access_token': 'fake-token-1'})
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {
            'sub': 'google-uid-unverified',
            'email': 'unverified@example.com',
            'email_verified': False,
            'name': 'Unverified User'
        })

        with self.client.session_transaction() as sess:
            sess['google_oauth_state'] = 'valid-state-999'

        response = self.client.get('/auth/google/callback?state=valid-state-999&code=valid_code', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        content = response.get_data(as_text=True)
        self.assertIn('Your Google email address is not verified by Google', content)

        # Ensure no user created
        user = User.query.filter_by(email='unverified@example.com').first()
        self.assertIsNone(user)

    @patch('requests.post')
    @patch('requests.get')
    def test_05_google_callback_new_user_creation(self, mock_get, mock_post):
        """Test first-time Google sign-in creates an active, verified account with no password."""
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {'access_token': 'fake-token-2'})
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {
            'sub': 'google-sub-10001',
            'email': 'newplayer@example.com',
            'email_verified': True,
            'name': 'Alice Wonder'
        })

        with self.client.session_transaction() as sess:
            sess['google_oauth_state'] = 'state-alice'

        response = self.client.get('/auth/google/callback?state=state-alice&code=valid_code', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check DB record
        user = User.query.filter_by(email='newplayer@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.google_id, 'google-sub-10001')
        self.assertTrue(user.is_verified)
        self.assertIsNotNone(user.verified_at)
        self.assertIsNone(user.password_hash)
        self.assertEqual(user.role, 'user')
        self.assertEqual(user.username, 'AliceWonder')

    @patch('requests.post')
    @patch('requests.get')
    def test_06_google_callback_account_linking(self, mock_get, mock_post):
        """Test existing registered user is linked via verified Google email without duplicate."""
        existing_user = User(
            username='bob_existing',
            email='bob@example.com',
            is_verified=False,
            role='user'
        )
        existing_user.set_password('SecretPassword123!')
        db.session.add(existing_user)
        db.session.commit()
        original_id = existing_user.id

        mock_post.return_value = MagicMock(status_code=200, json=lambda: {'access_token': 'fake-token-3'})
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {
            'sub': 'google-sub-bob-99',
            'email': 'bob@example.com',
            'email_verified': True,
            'name': 'Bob The Builder'
        })

        with self.client.session_transaction() as sess:
            sess['google_oauth_state'] = 'state-bob'

        response = self.client.get('/auth/google/callback?state=state-bob&code=valid_code', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check database: no new user was created, original user was updated
        users_count = User.query.filter_by(email='bob@example.com').count()
        self.assertEqual(users_count, 1)

        updated_user = db.session.get(User, original_id)
        self.assertEqual(updated_user.google_id, 'google-sub-bob-99')
        self.assertTrue(updated_user.is_verified)
        self.assertIsNotNone(updated_user.verified_at)
        # Original password preserved for dual login
        self.assertTrue(updated_user.check_password('SecretPassword123!'))

    @patch('requests.post')
    @patch('requests.get')
    def test_07_google_callback_existing_google_id(self, mock_get, mock_post):
        """Test returning user with existing google_id logs in seamlessly."""
        user = User(
            username='returning_google_user',
            email='returning@example.com',
            google_id='google-sub-already-saved',
            is_verified=True,
            role='user'
        )
        db.session.add(user)
        db.session.commit()

        mock_post.return_value = MagicMock(status_code=200, json=lambda: {'access_token': 'fake-token-4'})
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {
            'sub': 'google-sub-already-saved',
            'email': 'returning@example.com',
            'email_verified': True,
            'name': 'Returning User'
        })

        with self.client.session_transaction() as sess:
            sess['google_oauth_state'] = 'state-returning'

        response = self.client.get('/auth/google/callback?state=state-returning&code=valid_code', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        content = response.get_data(as_text=True)
        self.assertIn('Successfully signed in with Google', content)

    @patch('requests.post')
    @patch('requests.get')
    def test_08_google_callback_admin_blocked(self, mock_get, mock_post):
        """Test admin accounts are strictly blocked from signing in via Google OAuth."""
        admin = User(
            username='admin_boss',
            email='adminboss@example.com',
            role='admin',
            is_verified=True
        )
        admin.set_password('AdminPassword456!')
        db.session.add(admin)
        db.session.commit()

        mock_post.return_value = MagicMock(status_code=200, json=lambda: {'access_token': 'fake-token-5'})
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {
            'sub': 'google-sub-admin-attempt',
            'email': 'adminboss@example.com',
            'email_verified': True,
            'name': 'Admin Boss'
        })

        with self.client.session_transaction() as sess:
            sess['google_oauth_state'] = 'state-admin'

        response = self.client.get('/auth/google/callback?state=state-admin&code=valid_code', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        content = response.get_data(as_text=True)
        self.assertIn('Admin accounts cannot sign in via Google', content)

        # Admin must NOT have their google_id linked
        refreshed_admin = User.query.filter_by(username='admin_boss').first()
        self.assertIsNone(refreshed_admin.google_id)

    def test_09_google_user_forgot_password(self):
        """Test Google-only account on forgot-password shows friendly guidance."""
        google_user = User(
            username='google_only_forgot',
            email='gforgot@example.com',
            google_id='gid-123',
            password_hash=None,
            is_verified=True
        )
        db.session.add(google_user)
        db.session.commit()

        response = self.client.post('/auth/forgot-password', data={'email': 'gforgot@example.com'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        content = response.get_data(as_text=True)
        self.assertIn('This account signs in with Google and does not use a password', content)

    def test_10_google_user_change_password(self):
        """Test Google-only account trying /auth/change-password is informed and redirected."""
        google_user = User(
            username='google_only_change',
            email='gchange@example.com',
            google_id='gid-456',
            password_hash=None,
            is_verified=True
        )
        db.session.add(google_user)
        db.session.commit()

        # Log in the user directly
        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(google_user.id)
            sess['_fresh'] = True

        response = self.client.get('/auth/change-password', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        content = response.get_data(as_text=True)
        self.assertIn('Your account signs in with Google and does not use a password', content)

    def test_11_google_user_regular_login_warning(self):
        """Test Google-only account attempting password login receives a helpful prompt."""
        google_user = User(
            username='google_direct_login',
            email='gdirect@example.com',
            google_id='gid-789',
            password_hash=None,
            is_verified=True
        )
        db.session.add(google_user)
        db.session.commit()

        response = self.client.post('/auth/login', data={'username': 'google_direct_login', 'password': 'AnyPassword123'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        content = response.get_data(as_text=True)
        self.assertIn('This account signs in with Google', content)
        self.assertIn('Continue with Google', content)


if __name__ == '__main__':
    unittest.main()
