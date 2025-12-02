"""
HEADER_COMMENT_AUTOGEN
FILE: app\auth\routes.py
PURPOSE: Brief description of this file and where to edit it.

TIPS: Add your notes here to help future edits.
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from .forms import RegisterForm, LoginForm
from app.models import User, db

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken', 'warning')
            return render_template('auth/register.html', form=form)
        u = User(username=form.username.data, email=form.email.data)
        u.set_password(form.password.data)
        db.session.add(u); db.session.commit()
        flash('Account created. Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u and u.check_password(form.password.data):
            # Prevent admin login from user login page
            if u.is_admin():
                flash('Please use Admin Login page to login as admin', 'warning')
                return render_template('auth/login.html', form=form)
            login_user(u)
            flash('Logged in successfully', 'success')
            # Regular users go to quiz
            next_page = request.args.get('next') or url_for('quiz.select')
            return redirect(next_page)
        flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/admin/login', methods=['GET','POST'])
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
        if u and u.check_password(form.password.data):
            # Only allow admin users
            if not u.is_admin():
                flash('Access denied. This is for admin users only.', 'danger')
                return render_template('auth/admin_login.html', form=form)
            login_user(u)
            flash('Admin logged in successfully', 'success')
            return redirect(url_for('admin.index'))
        flash('Invalid username or password', 'danger')
    return render_template('auth/admin_login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('home'))
