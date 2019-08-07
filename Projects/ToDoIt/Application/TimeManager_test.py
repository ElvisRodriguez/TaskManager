import datetime
import os
import random
import sys
import unittest

import TimeManager


CURRENT_YEAR = datetime.datetime.now().year
CURRENT_MONTH = datetime.datetime.now().month
CURRENT_DAY = datetime.datetime.now().day
CURRENT_HOUR = datetime.datetime.now().hour
CURRENT_MINUTE = datetime.datetime.now().minute


class TestTimeManager(unittest.TestCase):
    def setUp(self):
        self.time_manager = TimeManager.TimeManager()
        self.invalid_date = '{year}-{month}-{day}'.format(
            year=(CURRENT_YEAR - 1),
            month=CURRENT_MONTH,
            day=CURRENT_DAY
        )
        self.valid_date = '{year}-{month}-{day}'.format(
            year=(CURRENT_YEAR + 1),
            month=CURRENT_MONTH,
            day=CURRENT_DAY
        )
        self.invalid_time = '{hour}:{minute}'.format(
            hour=(CURRENT_HOUR - 1),
            minute=CURRENT_MINUTE
        )
        self.valid_time = '{hour}:{minute}'.format(
            hour=(CURRENT_HOUR + 1),
            minute=CURRENT_MINUTE
        )

    def test_is_valid_date_with_invalid_date(self):
        self.assertFalse(self.time_manager.is_valid_date(self.invalid_date))

    def test_is_valid_date_with_valid_date(self):
        self.assertTrue(self.time_manager.is_valid_date(self.valid_date))

    def test_is_valid_time_with_invalid_time(self):
        self.assertFalse(self.time_manager.is_valid_time(self.invalid_time))

    def test_is_valid_time_with_valid_time(self):
        self.assertTrue(self.time_manager.is_valid_time(self.valid_time))

    def test_create_timestamp_with_invalid_datetime(self):
        self.time_manager.create_timestamp(self.invalid_date, self.invalid_time)
        self.assertIsNone(self.time_manager.timestamp)

    def test_create_timestamp_with_valid_datetime(self):
        self.time_manager.create_timestamp(self.valid_date, self.valid_time)
        timestamp = '{date} {time}'.format(
            date=self.valid_date, time=self.valid_time
        )
        self.assertIsNotNone(self.time_manager.timestamp)
        self.assertEqual(timestamp, self.time_manager.timestamp)


if __name__ == '__main__':
    with open('test_output.txt', 'a') as file:
        runner = unittest.TextTestRunner(stream=file, verbosity=2)
        unittest.main(testRunner=runner)
