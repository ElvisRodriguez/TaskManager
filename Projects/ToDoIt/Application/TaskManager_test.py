import datetime
import unittest

import TaskManager
import TimeManager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.task_manager = TaskManager.TaskManager('test.db')
        self.username = 'PythonUnittest'
        self.password = 'HorseEatsSugarCube'
        self.email = 'unittest@gmail.com'
        self.task = ('Write more tests!', '1993-12-11')
        self.unique_task = (
            'Do not re-use me!', '{year}-{month}-{day}'.format(
                year=TimeManager.CURRENT_YEAR,
                month=TimeManager.CURRENT_MONTH,
                day=TimeManager.CURRENT_DAY
            )
        )

    def retrieve_id(self):
        task_message, date = self.unique_task
        tasks = self.task_manager.retrieve_tasks(self.username)
        unique_task = None
        for task in tasks:
            if task_message in task and date in task:
                unique_task = task
        id = unique_task[0]
        return id

    def test_insert_new_task(self):
        task_message, date = self.task
        self.task_manager.insert_new_task(task_message, date, self.username)
        tasks = self.task_manager.retrieve_tasks(self.username)
        self.assertIsNotNone(tasks)
        message = 'Task should have been added to ToDoTable'
        actual_task = None
        for task in tasks:
            if task_message in task and date in task:
                actual_task = (task[1], task[2])
        self.assertIsNotNone(actual_task)
        self.assertEqual(self.task, actual_task, message)

    def test_retrieve_task_by_id(self):
        task_message, date = self.unique_task
        self.task_manager.insert_new_task(task_message, date, self.username)
        id = self.retrieve_id()
        retrieved_task = self.task_manager.retrieve_task_by_id(id)
        self.assertEqual(self.unique_task, retrieved_task)

    def test_remove_task_by_id(self):
        id = self.retrieve_id()
        self.unique_task = (id, self.unique_task[0], self.unique_task[1])
        self.task_manager.remove_task_by_id(id)
        tasks = self.task_manager.retrieve_tasks(self.username)
        self.assertNotIn(self.unique_task, tasks)

    def test_remove_task(self):
        task, date = self.task
        self.task_manager.remove_task(task, date, self.username)
        tasks = self.task_manager.retrieve_tasks(self.username)
        message = 'Task should have been removed from ToDoTable'
        self.assertNotIn(self.task, tasks, message)


if __name__ == '__main__':
    with open('test_output.txt', 'a') as file:
        runner = unittest.TextTestRunner(stream=file, verbosity=2)
        unittest.main(testRunner=runner)
