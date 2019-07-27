import flask_login
import hashlib
import sqlite3 as sql
import uuid


class User(flask_login.UserMixin):
    def __init__(self, username, database='todo_table.db'):
        self.id = None
        self.username = username
        self.database = database

    def hash_password(self, password):
        salt = uuid.uuid4().hex
        return hashlib.sha256(
            salt.encode() + password.encode()
        ).hexdigest() + ':' + salt

    def check_password(self, hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(
            salt.encode() + user_password.encode()
        ).hexdigest()

    def insert_new_user(self, password, email):
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        password = self.hash_password(password)
        try:
            cursor.execute(
                'INSERT INTO Users (Username, Password, Email) VALUES (?,?,?)',
                (self.username, password, email)
            )
            connection.commit()
            connection.close()
            return True
        except sql.IntegrityError:
            connection.close()
            return False

    def login_user(self, password):
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(
            'SELECT Username, Password FROM Users WHERE Username=?',
            (self.username,)
        )
        credentials = cursor.fetchone()
        connection.close()
        if self.username == credentials[0] and self.check_password(
            credentials[1], password
        ):
            return True
        return False

    def find_id(self):
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(
            'SELECT UserID FROM Users WHERE Username=?', (self.username,)
        )
        row = cursor.fetchone()
        connection.close()
        self.id = row[0]


def find_username_with_id(database, id):
    connection = sql.connect(database)
    cursor = connection.cursor()
    cursor.execute('SELECT Username FROM Users WHERE UserID=?', (id,))
    row = cursor.fetchone()
    connection.close()
    return row[0]
