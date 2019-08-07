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
        self.id = all_tasks[0][0]
        actual_task = (all_tasks[0][1], all_tasks[0][2])
        message = 'Task should have been added to ToDoTable'
        self.assertEqual(self.task, actual_task, message)

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
    with open('test_output.txt', 'a') as file:
        runner = unittest.TextTestRunner(stream=file, verbosity=2)
        unittest.main(testRunner=runner)
