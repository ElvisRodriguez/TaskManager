import flask

import TaskManager
import User

app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/', methods=['POST', 'GET'])
def home():
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        return flask.render_template('home.html', username=username)
    else:
        return flask.render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        email = flask.request.form['email']
        return flask.render_template('signup.html')
    else:
        return flask.render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
