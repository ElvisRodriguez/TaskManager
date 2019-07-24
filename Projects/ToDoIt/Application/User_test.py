import datetime
import unittest

import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User.User(database='test.db')
        self.username = 'PythonUnittest:{timestamp}'.format(
            timestamp=str(datetime.datetime.now()))
        self.password = 'HorseEatsSugarCube'
        self.email = 'unittest@gmail.com'

    def test_insert_new_user(self):
        self.assertTrue(
            self.user.insert_new_user(self.username, self.password, self.email)
        )

    def test_duplicate_new_user(self):
        username = 'PythonUnittest'
        self.assertFalse(
            self.user.insert_new_user(username, self.password, self.email)
        )

    def test_login_user(self):
        username = 'PythonUnittest'
        self.assertTrue(self.user.login_user(username, self.password))


if __name__ == '__main__':
    with open('test_output.txt', 'a') as file:
        runner = unittest.TextTestRunner(file)
        unittest.main(testRunner=runner)
