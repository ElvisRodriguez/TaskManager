from flask import escape, Flask, redirect, render_template, request, session, url_for
import flask_login
import os

import TaskManager
import User

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.urandom(16)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return render_template('home.html', username=username)
    else:
        return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        return render_template('signup.html')
    else:
        return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
