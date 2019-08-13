from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateTimeField, PasswordField, StringField,
                     SubmitField, TextAreaField
                     )
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    re_password = PasswordField(
        'Re-Enter Password', validators=[DataRequired()]
    )
    submit = SubmitField('Sign Up')


class CreateTaskForm(FlaskForm):
    task = TextAreaField('Task', validators=[DataRequired()])
    timestamp = DateTimeField('Date And Time', validators=[DataRequired()])
    submit = SubmitField('Create Task')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    re_password = PasswordField(
        'Re-Enter Password', validators=[DataRequired()]
    )
    submit = SubmitField('Submit')
