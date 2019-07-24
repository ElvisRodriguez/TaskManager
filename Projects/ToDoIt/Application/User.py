import flask_login
import hashlib
import sqlite3 as sql
import uuid


def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(
        salt.encode() + password.encode()
    ).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(
        salt.encode() + user_password.encode()
    ).hexdigest()


class User(flask_login.UserMixin):
    def __init__(self, database):
        self.database = database
        self.id = None

    def insert_new_user(self, username, password, email):
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        password = hash_password(password)
        try:
            cursor.execute(
                'INSERT INTO Users (Username, Password, Email) VALUES (?,?,?)',
                (username, password, email)
            )
            connection.commit()
            connection.close()
            self.id = username.encode('utf-8')
            return True
        except sql.IntegrityError:
            connection.close()
            return False

    def login_user(self, username, password):
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(
            'SELECT Username, Password FROM Users WHERE Username=?',
            (username,)
        )
        credentials = cursor.fetchone()
        connection.close()
        if username == credentials[0] and check_password(credentials[1], password):
            self.id = username.encode('utf-8')
            return True
        return False