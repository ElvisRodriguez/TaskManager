import datetime


class TimeManager(object):
    def __init__(self):
        self.timestamp = None

    def current_time(self):
        raw_time = datetime.datetime.now()
        current_time = [raw_time.hour, raw_time.minute]
        return ':'.join([str(value) for value in current_time])

    def current_date(self):
        raw_date = datetime.datetime.date()
        current_date = [raw_date.year, raw_date.month, raw_date.day]
        return '-'.join([str(value) for value in current_date])

    def is_valid_date(self, date):
        current_date = datetime.date.today()
        given_date = date.split('-')
        given_date = [int(value) for value in given_date]
        given_date = datetime.date(
            year=given_date[0], month=given_date[1], day=given_date[2]
        )
        if (given_date - current_date).days < 0:
            return False
        return True

    def is_valid_time(self, time):
        current_time = datetime.datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute
        given_time = time.split(':')
        given_hour = int(given_time[0])
        given_minute = int(given_time[1])
        if given_hour < current_hour:
            return False
        if given_hour == current_hour:
            if given_minute < current_minute:
                return False
        return True

    def create_timestamp(self, date, time):
        if self.is_valid_date(date) and self.is_valid_time(time):
            self.timestamp = '{date} {time}'.format(date=date, time=time)
