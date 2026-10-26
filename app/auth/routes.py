"""
HEADER_COMMENT_AUTOGEN
FILE: app\auth\routes.py
PURPOSE: Authentication routes — login, register, logout, forgot/reset password

TIPS: Rate limiting applied on login/register. Forgot password uses itsdangerous tokens.
"""

from flask import render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from app.models import User, db
from app import limiter, mail
import logging
import secrets
import hmac
import urllib.parse
import re

import os
import requests
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Built-in Disposable / Temporary Email Blocklist
# ──────────────────────────────────────────────
DISPOSABLE_EMAIL_DOMAINS = {
    'tempmail.com', 'throwawaymail.com', 'mailinator.com', '10minutemail.com',
    'guerrillamail.com', 'sharklasers.com', 'trashmail.com', 'getairmail.com',
    'yopmail.com', 'dispostable.com', 'temp-mail.org', 'fakeinbox.com',
    'generator.email', 'tempmailo.com', 'fakemailgenerator.com', 'nada.ltd',
    'mohmal.com', 'burnermail.io', 'inboxkitten.com', 'crazymailing.com',
    'emailondeck.com', 'mytemp.email', 'tempail.com', 'disposablemail.com'
}

def is_disposable_email(email):
    """Check if the email belongs to a disposable or throwaway domain."""
    if not email or '@' not in email:
        return False
    domain = email.split('@')[-1].strip().lower()
    return domain in DISPOSABLE_EMAIL_DOMAINS


# ──────────────────────────────────────────────
# Brevo HTTPS REST API Mail Sender (Render Free Tier)
# ──────────────────────────────────────────────
def send_email_via_brevo(to_email, to_name, subject, html_content, text_content=None):
    """
    Sends email using Brevo's HTTPS REST API.
    Bypasses Render's outbound SMTP block completely.
    Never crashes if Brevo fails; logs the error.
    """
    api_key = current_app.config.get('BREVO_API_KEY') or os.environ.get('BREVO_API_KEY')
    sender_email = (
        current_app.config.get('MAIL_SENDER_EMAIL') or
        os.environ.get('MAIL_SENDER_EMAIL') or
        current_app.config.get('MAIL_DEFAULT_SENDER') or
        'noreply@quizcraft.com'
    )
    sender_name = "QuizCraft"

    if not api_key:
        logger.warning("BREVO_API_KEY not set. Attempting Flask-Mail SMTP fallback...")
        try:
            from flask_mail import Message
            from app import mail
            msg = Message(subject=subject, sender=sender_email, recipients=[to_email])
            msg.body = text_content or html_content
            msg.html = html_content
            mail.send(msg)
            logger.info("Email sent via Flask-Mail fallback to %s", to_email)
            return True
        except Exception as e:
            logger.error("Fallback mail send failed: %s", e)
            return False

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }
    payload = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [{"email": to_email, "name": to_name or to_email}],
        "subject": subject,
        "htmlContent": html_content
    }
    if text_content:
        payload["textContent"] = text_content

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code in (200, 201, 202):
            logger.info("Brevo email sent successfully to %s", to_email)
            return True
        else:
            logger.error("Brevo API error (%d): %s", response.status_code, response.text)
            return False
    except Exception as e:
        logger.error("Brevo request failed: %s", e)
        return False


# ──────────────────────────────────────────────
# Helper: send account verification email
# ──────────────────────────────────────────────
def send_verification_email(user):
    """Generate 24-hour token and send verification email via Brevo REST API."""
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(user.email, salt='email-verify-salt')
    verify_url = url_for('auth.verify_email', token=token, _external=True)

    subject = "Verify your QuizCraft account"
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px;">
        <h2 style="color: #4f46e5; text-align: center; margin-bottom: 8px;">Welcome to QuizCraft! 🎯</h2>
        <p style="color: #475569; font-size: 15px;">Hi <strong>{user.username}</strong>,</p>
        <p style="color: #475569; font-size: 15px;">Thank you for registering. Please confirm your email address by clicking the button below:</p>
        <p style="text-align: center; margin: 28px 0;">
            <a href="{verify_url}" style="background-color: #4f46e5; color: #ffffff; padding: 12px 28px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 15px; display: inline-block;">Verify Email Address</a>
        </p>
        <p style="color: #64748b; font-size: 13px;">Or copy and paste this link in your browser:<br><a href="{verify_url}" style="color: #4f46e5;">{verify_url}</a></p>
        <p style="color: #64748b; font-size: 13px;">This verification link will expire in <strong>24 hours</strong>.</p>
        <p style="color: #e11d48; font-size: 13px; background-color: #fff1f2; padding: 10px; border-radius: 4px;">
            <strong>Note:</strong> Check your spam folder too if you do not see this email in your inbox.
        </p>
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;">
        <p style="color: #94a3b8; font-size: 12px; text-align: center;">QuizCraft — The Ultimate Quiz Platform</p>
    </div>
    """
    text_content = f"""Hi {user.username},

Thank you for registering on QuizCraft.
Please verify your email by opening the link below (valid for 24 hours):
{verify_url}

Note: Check your spam folder too if you do not see this email in your inbox.

— QuizCraft Team
"""
    return send_email_via_brevo(user.email, user.username, subject, html_content, text_content)


# ──────────────────────────────────────────────
# Helper: send password reset email
# ──────────────────────────────────────────────
def send_reset_email(user):
    """Generate 30-min token and send password reset email via Brevo REST API."""
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(user.email, salt='password-reset-salt')
    reset_url = url_for('auth.reset_password', token=token, _external=True)

    subject = "QuizCraft — Password Reset Request"
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px;">
        <h2 style="color: #4f46e5; text-align: center; margin-bottom: 8px;">Password Reset Request</h2>
        <p style="color: #475569; font-size: 15px;">Hi <strong>{user.username}</strong>,</p>
        <p style="color: #475569; font-size: 15px;">You requested to reset your QuizCraft password. Click the button below:</p>
        <p style="text-align: center; margin: 28px 0;">
            <a href="{reset_url}" style="background-color: #e11d48; color: #ffffff; padding: 12px 28px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 15px; display: inline-block;">Reset Password</a>
        </p>
        <p style="color: #64748b; font-size: 13px;">Or copy and paste this link in your browser:<br><a href="{reset_url}" style="color: #4f46e5;">{reset_url}</a></p>
        <p style="color: #64748b; font-size: 13px;">This reset link will expire in <strong>30 minutes</strong>.</p>
        <p style="color: #e11d48; font-size: 13px; background-color: #fff1f2; padding: 10px; border-radius: 4px;">
            <strong>Note:</strong> Check your spam folder too if you do not see this email in your inbox.
        </p>
        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;">
        <p style="color: #94a3b8; font-size: 12px; text-align: center;">If you did not request this, you can safely ignore this email.</p>
    </div>
    """
    text_content = f"""Hi {user.username},

You requested to reset your QuizCraft password.
Click the link below (valid for 30 minutes):
{reset_url}

Note: Check your spam folder too if you do not see this email in your inbox.
If you did not request this, please ignore this email.

— QuizCraft Team
"""
    return send_email_via_brevo(user.email, user.username, subject, html_content, text_content)


# ──────────────────────────────────────────────
# Profile
# ──────────────────────────────────────────────
@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')


# ──────────────────────────────────────────────
# Register
# ──────────────────────────────────────────────
@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        username_clean = form.username.data.strip()
        email_clean = form.email.data.strip().lower()

        # 1. Block disposable email domains
        if is_disposable_email(email_clean):
            flash('Temporary or disposable email addresses are not allowed. Please use a permanent email address.', 'danger')
            return render_template('auth/register.html', form=form)

        # 2. Check duplicate username or email
        if User.query.filter_by(username=username_clean).first():
            flash('Username already taken', 'warning')
            return render_template('auth/register.html', form=form)
        if User.query.filter_by(email=email_clean).first():
            flash('Email already registered', 'warning')
            return render_template('auth/register.html', form=form)

        # 3. Create user with is_verified = False
        u = User(username=username_clean, email=email_clean, is_verified=False)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()

        # 4. Send verification email via Brevo REST API (never crash registration on fail)
        try:
            send_verification_email(u)
        except Exception as e:
            logger.error("Error while dispatching verification email: %s", e)

        flash('Registration successful! We have sent a verification link to your email. Please verify your email to activate your account. Check your spam folder too.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


# ──────────────────────────────────────────────
# Verify Email Route
# ──────────────────────────────────────────────
@auth_bp.route('/verify-email/<token>')
def verify_email(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='email-verify-salt', max_age=86400)  # 24 hours
    except SignatureExpired:
        flash('The verification link has expired. Please request a new one.', 'danger')
        return render_template('auth/resend_verification.html')
    except BadSignature:
        flash('Invalid or corrupted verification link.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User account not found.', 'danger')
        return redirect(url_for('auth.login'))

    if user.is_verified:
        flash('Your email is already verified. Please login.', 'info')
        return redirect(url_for('auth.login'))

    user.is_verified = True
    user.verified_at = datetime.utcnow()
    db.session.commit()
    flash('Email verified successfully! You can now log in to QuizCraft.', 'success')
    return redirect(url_for('auth.login'))


from flask_limiter.util import get_remote_address

def get_resend_rate_limit_key():
    """Rate limit key combining client IP and submitted email address."""
    email = request.form.get('email', '').strip().lower() if request.method == 'POST' else ''
    ip = get_remote_address()
    return f"{ip}:{email}" if email else ip


# ──────────────────────────────────────────────
# Resend Verification Email
# ──────────────────────────────────────────────
@auth_bp.route('/resend-verification', methods=['GET', 'POST'])
@limiter.limit("3 per minute", methods=["POST"])
@limiter.limit("1 per minute", methods=["POST"], key_func=get_resend_rate_limit_key)
def resend_verification():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        if not email:
            flash('Please enter your email address.', 'warning')
            return render_template('auth/resend_verification.html')

        user = User.query.filter_by(email=email).first()
        # Only send email if account exists and is not yet verified
        if user and not user.is_verified:
            try:
                send_verification_email(user)
            except Exception as e:
                logger.error("Failed to resend verification email: %s", e)

        # Uniform message to prevent email enumeration (whether email exists, is verified, or non-existent)
        flash('If an unverified account with that email exists, a new verification link has been sent. Check your spam folder too.', 'info')
        return redirect(url_for('auth.login'))

    email_prefill = request.args.get('email', '')
    return render_template('auth/resend_verification.html', email=email_prefill)


# ──────────────────────────────────────────────
# Google OAuth 2.0 (OpenID Connect)
# ──────────────────────────────────────────────
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


@auth_bp.route('/google')
@limiter.limit("10 per minute")
def google_login():
    """Initiate Google OAuth 2.0 flow with CSRF state protection."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    client_id = current_app.config.get('GOOGLE_CLIENT_ID')
    client_secret = current_app.config.get('GOOGLE_CLIENT_SECRET')
    if not client_id or not client_secret:
        flash('Google Sign-In is not configured. Please contact the administrator.', 'warning')
        return redirect(url_for('auth.login'))

    # Generate cryptographically secure random state to prevent CSRF
    state = secrets.token_urlsafe(32)
    session['google_oauth_state'] = state

    redirect_uri = url_for('auth.google_callback', _external=True)
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state,
        'access_type': 'online',
        'prompt': 'select_account'
    }
    auth_url = f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)


@auth_bp.route('/google/callback')
@limiter.limit("10 per minute")
def google_callback():
    """Handle Google OAuth 2.0 callback, verify state, exchange token, and login user."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # 1. Handle error response from Google (e.g., user cancelled consent)
    error = request.args.get('error')
    if error:
        session.pop('google_oauth_state', None)
        logger.warning("Google OAuth error from provider: %s", error)
        flash('Google Sign-In was cancelled or denied.', 'warning')
        return redirect(url_for('auth.login'))

    # 2. Verify state token against session (CSRF protection)
    state = request.args.get('state')
    stored_state = session.pop('google_oauth_state', None)
    if not state or not stored_state or not hmac.compare_digest(state, stored_state):
        logger.warning("Google OAuth state mismatch or missing session state")
        flash('Invalid or expired authentication session. Please try again.', 'danger')
        return redirect(url_for('auth.login'))

    # 3. Verify authorization code is present
    code = request.args.get('code')
    if not code:
        logger.warning("Google OAuth callback missing authorization code")
        flash('Authorization code missing from Google. Please try again.', 'danger')
        return redirect(url_for('auth.login'))

    client_id = current_app.config.get('GOOGLE_CLIENT_ID')
    client_secret = current_app.config.get('GOOGLE_CLIENT_SECRET')
    if not client_id or not client_secret:
        flash('Google Sign-In configuration error.', 'danger')
        return redirect(url_for('auth.login'))

    # 4. Exchange authorization code for access token via HTTPS POST
    redirect_uri = url_for('auth.google_callback', _external=True)
    token_payload = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    try:
        token_resp = requests.post(GOOGLE_TOKEN_URL, data=token_payload, timeout=10)
        if token_resp.status_code != 200:
            logger.error("Failed to exchange Google OAuth code (HTTP %d)", token_resp.status_code)
            flash('Failed to authenticate with Google. Please try again.', 'danger')
            return redirect(url_for('auth.login'))

        token_data = token_resp.json()
        access_token = token_data.get('access_token')
        if not access_token:
            logger.error("No access_token returned by Google")
            flash('Failed to obtain authentication token from Google.', 'danger')
            return redirect(url_for('auth.login'))

        # 5. Fetch verified user profile from OpenID Connect userinfo endpoint
        headers = {'Authorization': f'Bearer {access_token}'}
        userinfo_resp = requests.get(GOOGLE_USERINFO_URL, headers=headers, timeout=10)
        if userinfo_resp.status_code != 200:
            logger.error("Failed to fetch Google userinfo (HTTP %d)", userinfo_resp.status_code)
            flash('Failed to retrieve profile information from Google.', 'danger')
            return redirect(url_for('auth.login'))

        userinfo = userinfo_resp.json()
    except Exception as e:
        logger.error("Google OAuth network or request exception: %s", e)
        flash('Unable to connect to Google. Please check your internet connection and try again.', 'danger')
        return redirect(url_for('auth.login'))

    # 6. Verify email_verified is true
    email_verified = userinfo.get('email_verified') in (True, 'true', 'True')
    if not email_verified:
        flash('Your Google email address is not verified by Google. Please verify your Google account first.', 'danger')
        return redirect(url_for('auth.login'))

    google_sub = str(userinfo.get('sub', '')).strip()
    google_email = str(userinfo.get('email', '')).strip().lower()
    google_name = str(userinfo.get('name') or userinfo.get('given_name') or '').strip()

    if not google_sub or not google_email:
        flash('Incomplete profile data received from Google.', 'danger')
        return redirect(url_for('auth.login'))

    # 7. Check if user exists by google_id
    user = User.query.filter_by(google_id=google_sub).first()

    # 8. If not found by google_id, check by verified email (Account Linking)
    if not user:
        user = User.query.filter_by(email=google_email).first()
        if user:
            # Block admin accounts from signing in via Google
            if user.is_admin() or user.role == 'admin':
                logger.warning("Admin account %s blocked from Google Sign-In", user.username)
                flash('Admin accounts cannot sign in via Google. Please use the Admin Login page.', 'danger')
                return redirect(url_for('auth.admin_login'))

            # Link Google ID to existing account and ensure verified
            user.google_id = google_sub
            user.is_verified = True
            if not user.verified_at:
                user.verified_at = datetime.utcnow()
            db.session.commit()
            logger.info("Linked Google account to existing user: %s", user.username)
            login_user(user)
            flash('Successfully signed in and linked your Google account!', 'success')
            next_page = request.args.get('next') or url_for('quiz.select')
            return redirect(next_page)

    # If user was found by google_id
    if user:
        # Block admin accounts from signing in via Google
        if user.is_admin() or user.role == 'admin':
            logger.warning("Admin account %s with google_id blocked from Google Sign-In", user.username)
            flash('Admin accounts cannot sign in via Google. Please use the Admin Login page.', 'danger')
            return redirect(url_for('auth.admin_login'))

        user.is_verified = True
        if not user.verified_at:
            user.verified_at = datetime.utcnow()
        db.session.commit()
        login_user(user)
        flash('Successfully signed in with Google!', 'success')
        next_page = request.args.get('next') or url_for('quiz.select')
        return redirect(next_page)

    # 9. Create new user account for first-time Google sign-in
    # Derive unique username from Google display name or email prefix (max 150 chars)
    base_name = re.sub(r'[^a-zA-Z0-9_]', '', google_name)
    if not base_name:
        base_name = re.sub(r'[^a-zA-Z0-9_]', '', google_email.split('@')[0])
    if not base_name:
        base_name = 'user'

    base_username = base_name[:140]
    username_candidate = base_username
    counter = 1
    while User.query.filter_by(username=username_candidate).first():
        username_candidate = f"{base_username[:135]}_{counter}"
        counter += 1

    new_user = User(
        username=username_candidate,
        email=google_email,
        password_hash=None,
        role='user',
        is_verified=True,
        verified_at=datetime.utcnow(),
        google_id=google_sub
    )
    db.session.add(new_user)
    db.session.commit()
    logger.info("Created new user via Google Sign-In: %s", username_candidate)
    login_user(new_user)
    flash('Welcome to QuizCraft! Your account has been created via Google.', 'success')
    return redirect(url_for('quiz.select'))


# ──────────────────────────────────────────────
# Login (User)
# ──────────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u:
            # Check if this is a Google-only account without password
            if not u.password_hash and u.google_id:
                flash('This account signs in with Google. Please use the "Continue with Google" button.', 'info')
                return render_template('auth/login.html', form=form)

            password_ok = u.check_password(form.password.data)

            if not password_ok and u.password_hash == form.password.data:
                # Legacy accounts stored plain-text passwords; upgrade hash in-place
                u.set_password(form.password.data)
                db.session.commit()
                password_ok = True

            if password_ok:
                # Prevent admin login from user login page
                if u.is_admin():
                    flash('Please use Admin Login page to login as admin', 'warning')
                    return render_template('auth/login.html', form=form)

                # Check if regular user email is verified
                if not u.is_verified:
                    flash('Your email is not verified yet. Please check your inbox (and spam folder too) or request a new verification link.', 'warning')
                    return render_template('auth/login.html', form=form, unverified_email=u.email)

                login_user(u)
                flash('Logged in successfully', 'success')
                next_page = request.args.get('next') or url_for('quiz.select')
                return redirect(next_page)
        flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)


# ──────────────────────────────────────────────
# Admin Login
# ──────────────────────────────────────────────
@auth_bp.route('/admin/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def admin_login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.index'))
        else:
            flash('You are logged in as a regular user. Please logout first.', 'warning')
            return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u:
            password_ok = u.check_password(form.password.data)

            if not password_ok and u.password_hash == form.password.data:
                # Upgrade legacy plain-text password for admin accounts as well
                u.set_password(form.password.data)
                db.session.commit()
                password_ok = True

            if password_ok:
                # Only allow admin users
                if not u.is_admin():
                    flash('Access denied. This is for admin users only.', 'danger')
                    return render_template('auth/admin_login.html', form=form)
                login_user(u)
                flash('Admin logged in successfully', 'success')
                return redirect(url_for('admin.index'))
        flash('Invalid username or password', 'danger')
    return render_template('auth/admin_login.html', form=form)


# ──────────────────────────────────────────────
# Forgot Password
# ──────────────────────────────────────────────
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
@limiter.limit("3 per minute")
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        # Always show success message (don't reveal if email exists), unless Google-only user
        if user:
            if not user.password_hash and user.google_id:
                flash('This account signs in with Google and does not use a password. Please use the "Continue with Google" button to log in.', 'info')
                return redirect(url_for('auth.login'))

            sent = send_reset_email(user)
            if not sent:
                flash('Could not send email. Please check mail configuration.', 'danger')
                return render_template('auth/forgot_password.html', form=form)
        flash('If an account with that email exists, a reset link has been sent. Check your inbox.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', form=form)


# ──────────────────────────────────────────────
# Reset Password (via token link)
# ──────────────────────────────────────────────
@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
    from flask import current_app
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=1800)  # 30 minutes
    except SignatureExpired:
        flash('The reset link has expired. Please request a new one.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    except BadSignature:
        flash('Invalid or tampered reset link.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password reset successfully! Please login with your new password.', 'success')
        if user.is_admin():
            return redirect(url_for('auth.admin_login'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form, token=token)


# ──────────────────────────────────────────────
# Change Password (logged in user)
# ──────────────────────────────────────────────
@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if not current_user.password_hash and current_user.google_id:
        flash('Your account signs in with Google and does not use a password. You can continue signing in with Google.', 'info')
        return redirect(url_for('home'))

    from .forms import ChangePasswordForm
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect', 'danger')
            return render_template('auth/change_password.html', form=form)
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password changed successfully', 'success')
        return redirect(url_for('home'))
    return render_template('auth/change_password.html', form=form)


# ──────────────────────────────────────────────
# Logout
# ──────────────────────────────────────────────
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('home'))
