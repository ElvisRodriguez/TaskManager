import datetime
import unittest

import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.username = 'PythonUnittest'
        self.user = User.User(self.username, database='test.db')
        self.unique_username = 'PythonUnittest:{timestamp}'.format(
            timestamp=str(datetime.datetime.now()))
        self.new_user = User.User(self.unique_username, database='test.db')
        self.password = 'HorseEatsSugarCube'
        self.email = 'unittest@gmail.com'

    def test_check_hashed_password(self):
        hashed_password = self.user.hash_password(self.password)
        self.assertTrue(
            self.user.check_password(hashed_password, self.password),
            msg='Hash method should always return the same result'
        )

    def test_insert_new_user(self):
        self.assertTrue(
            self.new_user.insert_new_user(self.password, self.email),
            msg='Username is always appended with the current time'
        )

    def test_duplicate_new_user(self):
        self.assertFalse(
            self.user.insert_new_user(self.password, self.email),
            msg='Username already exists in database, entries must be unique'
        )

    def test_login_user(self):
        self.assertTrue(
            self.user.login_user(self.password),
            msg='A failure indicates a tampering with test.db'
        )

    def test_login_with_incorrect_password(self):
        incorrect_password = 'HorseEatsSaltCube'
        self.assertFalse(
            self.user.login_user(incorrect_password),
            msg='Should always fail, this user/pass combo does not exist'
        )


if __name__ == '__main__':
    with open('test_output.txt', 'a') as file:
        runner = unittest.TextTestRunner(stream=file, verbosity=2)
        unittest.main(testRunner=runner)
