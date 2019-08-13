'''
Manages all users tasks in todo_table database.
'''
import sqlite3 as sql


class TaskManager(object):
    '''Manages insertion, deletion, and retrieval of tasks.
    '''

    def __init__(self, database='todo_table.db'):
        '''Initializes object with database name.

        Args:
            database: Name of database, this argument should be kept as the
                      default with the exception of this class' unit tests.

        Returns:
            None.
        '''
        self.database = database

    def retrieve_email(self, username: str) -> str:
        '''Retrieves a user's email from the database.

        Args:
            username: Username of user that email corresponds to.

        Returns:
            Email of user.
        '''
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute('SELECT Email FROM Users WHERE Username=?',
                       (username,)
                       )
        email = cursor.fetchone()[0]
        connection.close()
        return email

    def insert_new_task(self, task: str, date: str, username: str) -> None:
        '''Inserts a new task row into the database.

        Args:
            task: User's task, can be of variable length (single or multiline).
            date: Date of when user is to be reminded of their task. Is in the
                  format 'YYYY-MM-DD HH:MM'.
            username: Username of user.

        Returns:
            None.
        '''
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO ToDoTable (Task, TaskDate, Username) VALUES (?,?,?)',
            (task, date, username)
        )
        connection.commit()
        connection.close()

    def remove_task(self, task: str, date: str, username: str) -> None:
        '''Removes a task row from the database.

        Args:
            task: User's task, can be of variable length (single or multiline).
            date: Date of when user is to be reminded of their task. Is in the
                  format 'YYYY-MM-DD HH:MM'.
            username: Username of user.

        Returns:
            None.
        '''
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(
            'DELETE FROM ToDoTable WHERE Task=? AND TaskDate=? AND Username=?',
            (task, date, username)
        )
        connection.commit()
        connection.close()

    def remove_task_by_id(self, id: int) -> None:
        '''Removes a task row from the database.

        Args:
            id: ID of databse task row.

        Returns:
            None.
        '''
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute('DELETE FROM ToDoTable WHERE ToDoID=?', (id,))
        connection.commit()
        connection.close()

    def retrieve_tasks(self, username: str) -> list:
        '''Retrieves all tasks belonging to a user.

        Args:
            username: Username of user.

        Returns:
            A list of database rows (represented as 3-tuples).
        '''
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(
            'SELECT ToDoID, Task, TaskDate FROM ToDoTable WHERE Username=?',
            (username,)
        )
        all_tasks = cursor.fetchall()
        connection.close()
        return all_tasks

    def retrieve_task_by_id(self, id: int) -> list:
        '''Retrieves a task from the database with a row ID of id.

        Args:
            id: ID of task row.

        Returns:
            A list containing a single database row (represented as a 3-tuple).
        '''
        connection = sql.connect(self.database)
        cursor = connection.cursor()
        cursor.execute('SELECT Task, TaskDate FROM ToDoTable WHERE ToDoID=?',
                       (id,)
                       )
        task = cursor.fetchone()
        connection.close()
        return task
