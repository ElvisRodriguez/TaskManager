import sqlite3 as sql


class TaskManager(object):
    def __init__(self, database='todo_table.db'):
        self.database = database

    def retrieve_email(self, username):
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute('SELECT Email FROM Users WHERE Username=?',
                       (username,)
                       )
        email = cursor.fetchone()[0]
        connection.close()
        return email

    def insert_new_task(self, task, date, username):
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO ToDoTable (Task, TaskDate, Username) VALUES (?,?,?)',
            (task, date, username)
        )
        connection.commit()
        connection.close()

    def remove_task(self, task, date, username):
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(
            'DELETE FROM ToDoTable WHERE Task=? AND TaskDate=? AND Username=?',
            (task, date, username)
        )
        connection.commit()
        connection.close()

    def remove_task_by_id(self, id):
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute('DELETE FROM ToDoTable WHERE ToDoID=?', (id,))
        connection.commit()
        connection.close()

    def retrieve_tasks(self, username):
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(
            'SELECT ToDoID, Task, TaskDate FROM ToDoTable WHERE Username=?',
            (username,)
        )
        all_tasks = cursor.fetchall()
        connection.close()
        return all_tasks

    def retrieve_task_by_id(self, id):
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute('SELECT Task, TaskDate FROM ToDoTable WHERE ToDoID=?',
                       (id,)
                       )
        task = cursor.fetchone()
        connection.close()
        return task
