from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from models import db, User, Article, Issue
from forms import RegistrationForm, ArticleSubmissionForm
from config import Config
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    latest_articles = Article.query.order_by(Article.publication_date.desc()).limit(5).all()
    return render_template('index.html', latest_articles=latest_articles)

@app.route("/current_issue")
def current_issue():
    latest_issue = Issue.query.order_by(Issue.year.desc(), Issue.number.desc()).first()
    return render_template('current_issue.html', issue=latest_issue)

@app.route("/archive")
def archive():
    issues = Issue.query.order_by(Issue.year.desc(), Issue.number.desc()).all()
    return render_template('archive.html', issues=issues)

@app.route("/article/<int:article_id>")
def article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article.html', article=article)

@app.route("/submit_article", methods=['GET', 'POST'])
def submit_article():
    form = ArticleSubmissionForm()
    if form.validate_on_submit():
        # Handle article submission
        flash('Your article has been submitted for review', 'success')
        return redirect(url_for('index'))
    return render_template('submit_article.html', form=form)

@app.route("/for_authors")
def for_authors():
    return render_template('for_authors.html')

@app.route("/for_reviewers")
def for_reviewers():
    return render_template('for_reviewers.html')

@app.route("/for_readers")
def for_readers():
    return render_template('for_readers.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process form data
        flash('Account created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

def create_sample_data():
    # Create sample articles
    articles = [
        Article(title="The Impact of Climate Change on Biodiversity", 
                abstract="This study examines the effects of climate change on global biodiversity...",
                authors="John Doe, Jane Smith",
                keywords="climate change, biodiversity, ecology",
                publication_date="2023-09-01"),
        Article(title="Advancements in Quantum Computing", 
                abstract="Recent developments in quantum computing have opened new possibilities...",
                authors="Alice Johnson, Bob Wilson",
                keywords="quantum computing, technology, physics",
                publication_date="2023-08-15"),
        Article(title="The Role of Artificial Intelligence in Healthcare", 
                abstract="This paper explores the current and potential applications of AI in healthcare...",
                authors="Emily Brown, David Lee",
                keywords="artificial intelligence, healthcare, technology",
                publication_date="2023-07-30"),
    ]
    db.session.add_all(articles)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if Article.query.count() == 0:
            create_sample_data()
    app.run(host="0.0.0.0", port=5000)
