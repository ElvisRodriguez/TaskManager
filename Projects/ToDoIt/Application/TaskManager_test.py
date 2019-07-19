import random
import unittest

import TaskManager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.task_manager = TaskManager.TaskManager('test.db')
        self.username = 'PythonUnittest'
        self.password = 'HorseEatsSugarCube'
        self.email = 'unittest@gmail.com'
        self.task = ('Write more tests!', '12/11/1993')

    def test_insert_new_task(self):
        task = 'Write more tests!'
        date = '12/11/1993'
        self.task_manager.insert_new_task(task, date, self.username)
        all_tasks = self.task_manager.retrieve_tasks(self.username)
        message = 'Task should have been added to ToDoTable'
        self.assertIn(self.task, all_tasks, message)

    def test_remove_task(self):
        task = 'Write more tests!'
        date = '12/11/1993'
        self.task_manager.remove_task(task, date, self.username)
        all_tasks = self.task_manager.retrieve_tasks(self.username)
        message = 'Task should have been removed from ToDoTable'
        self.assertNotIn(self.task, all_tasks, message)

    def test_retrieve_email(self):
        result = self.task_manager.retrieve_email(self.username)
        message = 'Users email should exist in the database'
        self.assertEqual(self.email, result, message)


if __name__ == '__main__':
    unittest.main()
