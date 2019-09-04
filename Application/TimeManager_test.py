import datetime
import os
import random
import sys
import unittest

import TimeManager


class TestTimeManager(unittest.TestCase):
    def setUp(self):
        self.time_manager = TimeManager.TimeManager()
        self.invalid_date = '{year}-{month}-{day}'.format(
            year=(TimeManager.CURRENT_YEAR - 1),
            month=TimeManager.CURRENT_MONTH,
            day=TimeManager.CURRENT_DAY
        )
        self.valid_date = '{year}-{month}-{day}'.format(
            year=(TimeManager.CURRENT_YEAR + 1),
            month=TimeManager.CURRENT_MONTH,
            day=TimeManager.CURRENT_DAY
        )
        self.invalid_time = '{hour}:{minute}'.format(
            hour=(TimeManager.CURRENT_HOUR - 1),
            minute=TimeManager.CURRENT_MINUTE
        )
        self.valid_time = '{hour}:{minute}'.format(
            hour=(TimeManager.CURRENT_HOUR + 1),
            minute=TimeManager.CURRENT_MINUTE
        )
        self.current_date = '{year}-{month}-{day}'.format(
            year=TimeManager.CURRENT_YEAR,
            month=TimeManager.CURRENT_MONTH,
            day=TimeManager.CURRENT_DAY
        )
        self.current_time = '{hour}:{minute}'.format(
            hour=TimeManager.CURRENT_HOUR,
            minute=TimeManager.CURRENT_MINUTE
        )

    def test_current_date(self):
        current_date = TimeManager.TimeManager.current_date()
        self.assertEqual(current_date, self.current_date)

    def test_current_time(self):
        current_time = TimeManager.TimeManager.current_time()
        self.assertEqual(current_time, self.current_time)

    def test_create_datetime_object(self):
        test_datetime = datetime.datetime(
            TimeManager.CURRENT_YEAR,
            TimeManager.CURRENT_MONTH,
            TimeManager.CURRENT_DAY,
            TimeManager.CURRENT_HOUR,
            TimeManager.CURRENT_MINUTE
        )
        datetime_object = TimeManager.TimeManager.create_datetime_object(
            self.current_date, self.current_time
        )
        self.assertEqual(test_datetime.year, datetime_object.year)
        self.assertEqual(test_datetime.month, datetime_object.month)
        self.assertEqual(test_datetime.day, datetime_object.day)
        self.assertEqual(test_datetime.hour, datetime_object.hour)
        self.assertEqual(test_datetime.minute, datetime_object.minute)

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
