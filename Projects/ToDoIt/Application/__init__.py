from flask import escape, flash, Flask, redirect, render_template, request
from flask import send_from_directory, session, url_for
from flask_bootstrap import Bootstrap
from flask_login import current_user, login_user, LoginManager, login_required
from flask_login import logout_user

import os
import sqlite3 as sql

import EmailManager
import forms
import ItemTable
import TaskManager
import TimeManager
import User


DATABASE = 'todo_table.db'


app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.urandom(16))
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def user_loader(user_id):
    username = User.User.find_username_with_id(DATABASE, user_id)
    user = User.User(username)
    return user


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    username = current_user.username.title()
    task_manager = TaskManager.TaskManager()
    table = None
    all_tasks = task_manager.retrieve_tasks(username)
    if all_tasks:
        items = ItemTable.objectify(all_tasks)
        table = ItemTable.ItemTable(items)
    if request.method == 'GET':
        if table:
            return render_template('index.html', username=username, table=table)
        return render_template('index.html', username=username)
    if request.method == 'POST':
        error = None
        time_manager = TimeManager.TimeManager()
        task = request.form['task']
        date = request.form['date']
        time = request.form['time']
        if not time_manager.create_timestamp(date, time):
            error = 'Date/Time must be after current Date/Time'
            return render_template('index.html', username=username, error=error)
        timestamp = time_manager.timestamp
        task_manager.insert_new_task(task, timestamp, username)
        all_tasks = task_manager.retrieve_tasks(username)
        if all_tasks:
            items = ItemTable.objectify(all_tasks)
            table = ItemTable.ItemTable(items)
            return render_template('index.html', username=username, table=table)
        return render_template('index.html', username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = User.User(username=username)
        if user.login_user(password):
            user.find_id()
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        error = None
        username = request.form['username']
        password = request.form['password']
        re_entered_password = request.form['re_password']
        email = request.form['email']
        if password != re_entered_password:
            error = 'Passwords do not match'
            return render_template('signup.html', error=error)
        user = User.User(username)
        if user.insert_new_user(password, email):
            user.find_id()
            login_user(user)
            return redirect(url_for('index'))
        else:
            error = 'Username taken'
            return render_template('signup.html', error=error)
    return render_template('signup.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/remove_task', methods=['POST'])
@login_required
def remove_task():
    username = current_user.username
    task_manager = TaskManager.TaskManager()
    id = request.args['id']
    task_manager.remove_task_by_id(id)
    all_tasks = task_manager.retrieve_tasks(username)
    table = None
    if all_tasks:
        items = ItemTable.objectify(all_tasks)
        table = ItemTable.ItemTable(items)
        return redirect(url_for('index', username=username, table=table))
    return redirect(url_for('index', username=username))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        username = User.User.find_username_with_email(DATABASE, email)
        id = User.User.find_id_with_username(DATABASE, username)
        if username and id:
            user = User.User(username)
            secret_key = app.config['SECRET_KEY']
            token = user.get_reset_password_token(secret_key, id)
            url = url_for('reset_password', token=token, _external=True)
            password = None
            with open('passwords.txt', 'r') as file:
                password = file.readline()[:-1]
            email_manager = EmailManager.EmailManager(password=password)
            email_manager.create_password_reset_message(username, url)
            email_manager.send_email(email)
            return redirect(url_for('login'))
        error = 'Email does not exist'
        return render_template('reset_password_request.html', error=error)
    return render_template('reset_password_request.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    secret_key = app.config['SECRET_KEY']
    error = None
    id = User.User.verify_reset_password_token(token, secret_key)
    if id is None:
        error = 'Invalid Token, may be expired.'
        return url_for('index', error=error)
    if request.method == 'POST':
        username = User.User.find_username_with_id(DATABASE, id)
        user = User.User(username)
        new_password = request.form['password']
        re_new_password = request.form['re_password']
        if new_password != re_new_password:
            error = 'Passwords do not match'
            return url_for('index', error=error)
        if user.reset_password(new_password):
            return redirect(url_for('login'))
        error = 'New Password cannot be old password'
        return url_for('index', error=error)
    return render_template('reset_password.html', token=token)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'), 'favicon.ico'
    )


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
