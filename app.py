from flask import Flask, render_template, request, redirect, session, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import models and other modules after initializing db and login_manager
from models import User, Article, Issue
from forms import RegistrationForm, LoginForm, ArticleSubmissionForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    submitted_articles = user.submitted_articles
    published_articles = [article for article in submitted_articles if article.status == 'published']
    return render_template('dashboard.html', user=user, submitted_articles=submitted_articles, published_articles=published_articles)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.username = request.form['username']
        current_user.email = request.form['email']
        current_user.affiliation = request.form['affiliation']
        current_user.research_interests = request.form['research_interests']
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('edit_profile.html', user=current_user)

@app.route('/view_article/<int:article_id>')
@login_required
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('view_article.html', article=article)

@app.route('/download_article/<int:article_id>')
@login_required
def download_article(article_id):
    article = Article.query.get_or_404(article_id)
    return send_file(article.pdf_path, as_attachment=True)

# ...