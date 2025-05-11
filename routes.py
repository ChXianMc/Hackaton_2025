import os
import secrets
from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from app import app, db
from models import User
from forms import LoginForm, ForgotPasswordForm, ResetPasswordForm


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('dashboard')
        
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    # Placeholder for dashboard - we would implement this in a real system
    # For now we'll just show a success message
    return render_template('base.html', title='Dashboard', 
                          content=f'<div class="alert alert-success">Welcome {current_user.username}! You are now logged in.</div>')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            # Generate token and set expiry time (24 hours from now)
            token = secrets.token_hex(16)
            user.password_reset_token = token
            user.password_reset_expires = datetime.utcnow() + timedelta(hours=24)
            db.session.commit()
            
            # In a real-world scenario, you would send an email with reset link
            # For demo purposes, we'll just show the token
            reset_url = url_for('reset_password', token=token, _external=True)
            flash(f'Password reset requested. In a real system, an email would be sent with a reset link.', 'info')
            
            # For demonstration only - would not show this in production
            flash(f'Reset link would be: {reset_url}', 'info')
        else:
            # Don't reveal if user exists for security reasons
            flash('If that email address is in our system, a password reset link has been sent.', 'info')
        
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html', title='Forgot Password', form=form)


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    user = User.query.filter_by(password_reset_token=token).first()
    
    # Check if token is valid and not expired
    if not user or not user.password_reset_expires or user.password_reset_expires < datetime.utcnow():
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('forgot_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.password_reset_token = None
        user.password_reset_expires = None
        db.session.commit()
        flash('Your password has been reset successfully. You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', title='Reset Password', form=form)


# Create test users function - will be called after database initialization
def create_test_users():
    try:
        # Check if any users exist
        user_count = db.session.query(db.func.count(User.id)).scalar()
        if user_count == 0:
            # Create admin user
            admin = User(username='admin', email='admin@healthcare.org', role='admin')
            admin.set_password('password123')
            
            # Create doctor user
            doctor = User(username='doctor', email='doctor@healthcare.org', role='doctor')
            doctor.set_password('password123')
            
            # Create patient user
            patient = User(username='patient', email='patient@healthcare.org', role='patient')
            patient.set_password('password123')
            
            db.session.add_all([admin, doctor, patient])
            db.session.commit()
            print("Test users created successfully")
    except Exception as e:
        print(f"Error creating test users: {e}")
        db.session.rollback()
