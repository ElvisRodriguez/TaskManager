from flask import escape, flash, Flask, redirect, render_template, request
from flask import session, url_for
from flask_login import current_user, login_user, LoginManager, login_required
from flask_login import logout_user

import os
import sqlite3 as sql

import TaskManager
import User


app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.urandom(16))
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def user_loader(user_id):
    username = User.find_username_with_id('todo_table.db', user_id)
    user = User.User(username)
    return user


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    username = current_user.username.title()
    if request.method == 'GET':
        return render_template('index.html', username=username)
    if request.method == 'POST':
        task = request.form['task']
        date = request.form['date']
        time = request.form['time']
        print('{} @ {}|{}'.format(task, date, time))
        return render_template('index.html', username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.User(username=username)
        if user.login_user(password):
            user.find_id()
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')


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


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
