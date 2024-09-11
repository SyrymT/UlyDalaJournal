from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    affiliation = db.Column(db.String(200), nullable=False)
    research_interests = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    orcid = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    volume = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    articles = db.relationship('Article', backref='issue', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
