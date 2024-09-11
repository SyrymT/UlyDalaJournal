from app import app, db
from flask import render_template, flash, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFError
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
from extensions import login_manager, migrate
from config import Config
from models import User, Article, Issue  # Import the User model
from forms import RegistrationForm, LoginForm, ArticleSubmissionForm
from datetime import datetime, timedelta
from werkzeug.urls import url_parse
import logging
import os

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Initialize extensions
login_manager.init_app(app)
migrate.init_app(app, db)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_TYPE'] = 'filesystem'

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    app.logger.info("Index route accessed")
    latest_articles = Article.query.order_by(Article.publication_date.desc()).limit(5).all()
    return render_template('index.html', latest_articles=latest_articles, app=app)

@app.route("/current_issue")
def current_issue():
    # You can implement the logic for displaying the current issue here
    return render_template('current_issue.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    app.logger.info("Register route accessed")
    if current_user.is_authenticated:
        app.logger.info(f"User {current_user.username} is already authenticated")
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        app.logger.info(f"Registration form submitted for username: {form.username.data}")
        try:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
                full_name=form.full_name.data
            )
            db.session.add(user)
            db.session.commit()
            app.logger.info(f"User {user.username} created successfully")
            login_user(user)
            app.logger.info(f"User {user.username} logged in after registration")
            flash(f'Welcome, {user.full_name}! Your account has been created.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error during registration: {str(e)}")
            flash(f'An error occurred during registration: {str(e)}', 'danger')
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    app.logger.info("Login route accessed")
    if current_user.is_authenticated:
        app.logger.info(f"User {current_user.username} is already authenticated")
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        app.logger.info(f"Login form submitted for email: {form.email.data}")
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            app.logger.info(f"User {user.username} logged in successfully")
            next_page = request.args.get('next')
            if next_page and url_parse(next_page).netloc == '':
                app.logger.info(f"Redirecting to {next_page}")
                return redirect(next_page)
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('index'))
        else:
            app.logger.warning(f"Failed login attempt for email: {form.email.data}")
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
    app.logger.info(f"User {current_user.username} logged out")
    logout_user()
    return redirect(url_for('index'))

@app.route("/submit_article", methods=['GET', 'POST'])
@login_required
def submit_article():
    app.logger.info(f"Submit article accessed by user: {current_user.username}")
    form = ArticleSubmissionForm()
    if form.validate_on_submit():
        # Handle article submission
        flash('Your article has been submitted for review', 'success')
        return redirect(url_for('index'))
    return render_template('submit_article.html', form=form)

@app.route('/debug_session')
def debug_session():
    return {
        'is_authenticated': current_user.is_authenticated,
        'user_id': current_user.get_id() if current_user.is_authenticated else None,
        'session': dict(session)
    }

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400

@app.route("/archive")
def archive():
    # Implement the logic for the archive page
    return render_template('archive.html')

@app.route("/for_authors")
def for_authors():
    # Implement the logic for the 'For Authors' page
    return render_template('for_authors.html')

@app.route("/for_reviewers")
def for_reviewers():
    # Implement the logic for the 'For Reviewers' page
    return render_template('for_reviewers.html')

@app.route("/for_readers")
def for_readers():
    # Implement the logic for the 'For Readers' page
    return render_template('for_readers.html')

@app.route("/article/<int:article_id>")
def article(article_id):
    # Retrieve the article based on the article_id
    article = Article.query.get(article_id)
    return render_template('article.html', article=article)

@app.context_processor
def inject_app():
    return dict(app=app)

def create_sample_data():
    # Create sample users
    user1 = User(username='user1', email='user1@example.com', password_hash=bcrypt.generate_password_hash('password1').decode('utf-8'))
    user2 = User(username='user2', email='user2@example.com', password_hash=bcrypt.generate_password_hash('password2').decode('utf-8'))
    db.session.add_all([user1, user2])
    db.session.commit()

    # Create sample articles
    article1 = Article(title='Article 1', abstract='Abstract 1', authors='Author 1', user=user1)
    article2 = Article(title='Article 2', abstract='Abstract 2', authors='Author 2', user=user2)
    db.session.add_all([article1, article2])
    db.session.commit()

    # Create sample issues
    issue1 = Issue(volume=1, number=1, year=2023)
    issue2 = Issue(volume=1, number=2, year=2023)
    db.session.add_all([issue1, issue2])
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        # Check if there are any users in the database
        if User.query.count() == 0:
            # Create a test user if no users exist
            hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
            test_user = User(username='testuser', email='test@example.com', password_hash=hashed_password)
            db.session.add(test_user)
            db.session.commit()
        
        # Check if there are any articles in the database
        if Article.query.count() == 0:
            # Create sample data if no articles exist
            create_sample_data()
    app.run(host="0.0.0.0", port=5000, debug=True)
