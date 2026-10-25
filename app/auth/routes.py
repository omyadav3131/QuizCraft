"""
HEADER_COMMENT_AUTOGEN
FILE: app\auth\routes.py
PURPOSE: Authentication routes — login, register, logout, forgot/reset password

TIPS: Rate limiting applied on login/register. Forgot password uses itsdangerous tokens.
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from app.models import User, db
from app import limiter, mail
import logging

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Helper: send password reset email
# ──────────────────────────────────────────────
def send_reset_email(user):
    from itsdangerous import URLSafeTimedSerializer
    from flask_mail import Message
    from flask import current_app
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(user.email, salt='password-reset-salt')
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    try:
        msg = Message(
            subject='QuizCraft — Password Reset Request',
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@quizcraft.com'),
            recipients=[user.email]
        )
        msg.body = f"""Hi {user.username},

You requested a password reset for your QuizCraft account.
Click the link below to reset your password (valid for 30 minutes):

{reset_url}

If you did not request this, please ignore this email.

— QuizCraft Team
"""
        mail.send(msg)
        return True
    except Exception as e:
        logger.error("Mail send error: %s", e)
        return False


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
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken', 'warning')
            return render_template('auth/register.html', form=form)
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'warning')
            return render_template('auth/register.html', form=form)
        u = User(username=form.username.data, email=form.email.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('Account created. Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


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
        # Always show success message (don't reveal if email exists)
        if user:
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
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form, token=token)


# ──────────────────────────────────────────────
# Change Password (logged in user)
# ──────────────────────────────────────────────
@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
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
