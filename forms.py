from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class ArticleSubmissionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    abstract = TextAreaField('Abstract', validators=[DataRequired()])
    authors = StringField('Authors', validators=[DataRequired()])
    keywords = StringField('Keywords')
    pdf_file = FileField('PDF File', validators=[DataRequired()])
    submit = SubmitField('Submit Article')
