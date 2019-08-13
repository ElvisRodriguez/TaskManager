'''
Subclasses of flask_wtf.FlaskForm used to generate HTML forms in corresponding
app endpoints.
'''
from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateTimeField, PasswordField, StringField,
                     SubmitField, TextAreaField
                     )
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    '''Creates a standard HTML Login form using wtforms form fields.

    Attributes:
        username: A form field that accepts a required username (string).
        password: A form field that accepts a required password (unicode).
        remember_me: A form checkbox that tells the apps Login Manager if the
                     user's credentials should be remembered for future
                     sessions.
        submit: A submit button for the form.
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    '''Creates a standard HTML Sign Up form using wtforms form fields.

    Attributes:
        email: A form field that accepts a required email (string).
        username: A form field that accepts a required username (string).
        password: A form field that accepts a required password (unicode).
        re_password: A form field that accepts the same password (unicode) that
                     was given to the 'password' attribute.
        submit: A submit button for the form.
    '''
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    re_password = PasswordField(
        'Re-Enter Password', validators=[DataRequired()]
    )
    submit = SubmitField('Sign Up')


class CreateTaskForm(FlaskForm):
    '''Creates an HTML form to take a Users task and timestamp of task due date.

    Attributes:
        task: A form field that accepts a required single or multiline task
              description (string).
        timestamp: A form field that accepts a timestamp of the format
                   'YYYY-MM-DD HH:MM' representing when the User is to be
                   notified of the task.
        submit: A submit button for the form.
    '''
    task = TextAreaField('Task', validators=[DataRequired()])
    timestamp = DateTimeField(
        'Date And Time, Enter as \'YYYY-MM-DD HH:MM\'',
        format='%Y-%m-%d %H:%M',
        validators=[DataRequired()]
    )
    submit = SubmitField('Create Task')


class PasswordResetRequestForm(FlaskForm):
    '''Creates an HTML form for a password reset request.

    Attributes:
        email: A form field that accepts a required email (string).
        submit: A submit button for the form.
    '''
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PasswordResetForm(FlaskForm):
    '''Creates an HTML form for a password reset.

    Attributes:
        password: A form field that accepts a required password (unicode).
        re_password: A form field that accepts the same password (unicode) that
                     was given to the 'password' attribute.
        submit: A submit button for the form.
    '''
    password = PasswordField('Password', validators=[DataRequired()])
    re_password = PasswordField(
        'Re-Enter Password', validators=[DataRequired()]
    )
    submit = SubmitField('Submit')
