import datetime
import unittest

import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.username = 'PythonUnittest'
        self.database = 'test.db'
        self.user = User.User(self.username, database=self.database)
        self.unique_username = 'PythonUnittest:{timestamp}'.format(
            timestamp=str(datetime.datetime.now()))
        self.new_user = User.User(self.unique_username, database=self.database)
        self.password = 'HorseEatsSugarCube'
        self.email = 'unittest@gmail.com'

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

    def test_find_id(self):
        self.user.find_id()
        self.assertIsNotNone(self.user.id)
        self.assertIsInstance(self.user.id, int)

    def test_retrieve_email(self):
        result = self.user.retrieve_email()
        message = 'Users email should exist in the database'
        self.assertEqual(self.email, result, message)

    def test_reset_password_with_same_password(self):
        result = self.user.reset_password(self.password)
        self.assertFalse(result)

    def test_reset_password_with_new_password(self):
        new_password = 'HorseEatsSaltCube'
        result = self.user.reset_password(new_password)
        self.assertTrue(result)
        result = self.user.reset_password(self.password)
        self.assertTrue(result)

    def test_find_username_with_email(self):
        username = User.User.find_username_with_email(self.database, self.email)
        self.assertEqual(username, self.username)

    def test_find_username_with_id(self):
        id = User.User.find_id_with_username(self.database, self.username)
        username = User.User.find_username_with_id(self.database, id)
        self.assertEqual(username, self.username)


if __name__ == '__main__':
    with open('test_output.txt', 'a') as file:
        runner = unittest.TextTestRunner(stream=file, verbosity=2)
        unittest.main(testRunner=runner)
