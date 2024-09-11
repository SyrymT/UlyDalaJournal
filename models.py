from datetime import datetime
from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100))  # Add the full_name attribute
    affiliation = db.Column(db.String(100))
    research_interests = db.Column(db.String(200))
    submitted_articles = db.relationship('Article', backref='author', lazy=True)
    # ... other fields ...

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    authors = db.Column(db.String(200), nullable=False)
    keywords = db.Column(db.String(200))
    pdf_path = db.Column(db.String(255))
    publication_date = db.Column(db.DateTime)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('articles', lazy=True), overlaps="author,submitted_articles")

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    volume = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    articles = db.relationship('Article', backref='issue', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
