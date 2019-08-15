'''
Manages timestamps and date/time retrieved from users and database.
'''
import datetime


class TimeManager(object):
    '''Generates timestamps and date/times as well as verfies timestamps.
    '''

    def __init__(self) -> None:
        '''Initializes object with empty attributes timestamp and _days_ahead.

        Args:
            None.

        Returns:
            None.
        '''
        self.timestamp = None
        self._days_ahead = None

    @staticmethod
    def current_time() -> str:
        '''Retrieves the current time from datetime.datetime object.

        Args:
            None.

        Returns:
            String with the time formatted as 'HH:MM'.
        '''
        raw_time = datetime.datetime.now()
        current_time = [raw_time.hour, raw_time.minute]
        return ':'.join([str(value) for value in current_time])

    @staticmethod
    def current_date() -> str:
        '''Retrieves the current date from datetime.datetime object.

        Args:
            None.

        Returns:
            String with the date formatted as 'YYYY-MM-DD'.
        '''
        raw_date = datetime.datetime.now()
        current_date = [raw_date.year, raw_date.month, raw_date.day]
        return '-'.join([str(value) for value in current_date])

    @staticmethod
    def create_datetime_object(date: str, time: str) -> datetime.datetime:
        '''Creates a datetime object from date and time string representations.

        Args:
            date: String representing a date in the format 'YYYY-MM-DD'.
            time: String representing a time in the format 'HH:MM'.

        Returns:
            A datetime.datetime object with the given date and time.
        '''
        year, month, day = [int(value) for value in date.split('-')]
        hour, minute = [int(value) for value in time.split(':')]
        datetime_object = datetime.datetime(year, month, day, hour, minute)
        return datetime_object

    def is_valid_date(self, date: str) -> bool:
        '''Checks if date given is ahead of or is current date.

        Args:
            date: Date in the format 'YYYY-MM-DD' provided by user.

        Returns:
            True if date is ahead of or is current date, False otherwise.
        '''
        current_date = datetime.date.today()
        date_components = date.split('-')
        year, month, day = [int(component) for component in date_components]
        given_date = datetime.date(year, month, day)
        self._days_ahead = (given_date - current_date).days
        if self._days_ahead < 0:
            return False
        return True

    def is_valid_time(self, time: str) -> bool:
        '''Checks if time given is ahead of current time.

        Args:
            time: Time in the format 'HH:MM' provided by user.

        Returns:
            True if time is ahead of current time, False otherwise.
        '''
        if self._days_ahead is not None:
            if self._days_ahead > 0:
                return True
        current_time = datetime.datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute
        given_hour, given_minute = [int(value) for value in time.split(':')]
        if given_hour < current_hour:
            return False
        if given_hour == current_hour:
            if given_minute < current_minute:
                return False
        return True

    def create_timestamp(self, date: str, time: str) -> bool:
        '''Creates a timestamp with given date and time.

        Args:
            date: Date in the format 'YYYY-MM-DD' provided by user.
            time: Time in the fomat 'HH:MM' provided by user.

        Returns:
            True if a timestamp is created (i.e. both the date and time are
            valid) else False.
        '''
        if self.is_valid_date(date) and self.is_valid_time(time):
            self.timestamp = '{date} {time}'.format(date=date, time=time)
            return True
        return False
