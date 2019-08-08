import flask_login
import hashlib
import jwt
import sqlite3 as sql
import time
import uuid


class User(flask_login.UserMixin):
    def __init__(self, username, database='todo_table.db'):
        self.id = None
        self.username = username
        self.database = database

    def __hash_password(self, password):
        salt = uuid.uuid4().hex
        return hashlib.sha256(
            salt.encode() + password.encode()
        ).hexdigest() + ':' + salt

    def __check_password(self, hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(
            salt.encode() + user_password.encode()
        ).hexdigest()

    def insert_new_user(self, password, email):
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        password = self.__hash_password(password)
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
        if self.username == credentials[0] and self.__check_password(
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

    def reset_password(self, new_password):
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(
            'SELECT Password FROM Users WHERE Username=?',
            (self.username,)
        )
        row = cursor.fetchone()
        old_password = row[0]
        if self.__check_password(old_password, new_password):
            return False
        new_password = self.__hash_password(new_password)
        cursor.execute(
            'UPDATE Users SET Password=? WHERE Username=?',
            (new_password, self.username)
        )
        connection.commit()
        connection.close()
        return True

    def get_reset_password_token(self, secret_key, id, expires_in=60000):
        self.id = id
        return jwt.encode(
            {'reset_password': self.id, 'exp': time.time() + expires_in},
            secret_key, algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def find_username_with_email(database, email):
        connection = sql.connect(database)
        cursor = connection.cursor()
        cursor.execute('SELECT Username FROM Users WHERE Email=?', (email,))
        row = cursor.fetchone()
        connection.close()
        if row:
            username = row[0]
            return username
        return None

    @staticmethod
    def find_username_with_id(database, id):
        connection = sql.connect(database)
        cursor = connection.cursor()
        cursor.execute('SELECT Username FROM Users WHERE UserID=?', (id,))
        row = cursor.fetchone()
        connection.close()
        if row:
            username = row[0]
            return username
        return None

    @staticmethod
    def find_id_with_username(database, username):
        connection = sql.connect(database)
        cursor = connection.cursor()
        cursor.execute('SELECT UserID FROM Users WHERE Username=?', (username,))
        row = cursor.fetchone()
        connection.close()
        if row:
            id = row[0]
            return id
        return None

    @staticmethod
    def verify_reset_password_token(token, secret_key):
        try:
            id = jwt.decode(token, secret_key,
                            algorithms=['HS256'])['reset_password']
        except:
            return None
        return id
