from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import getpass
import os
import smtplib
import ssl
import sys


TEST_MESSAGE_HTML = '''
<html>
  <body>
    {status}
    <p>
      {message}
    </p>
  </body>
</html>
'''

STATUS_MESSAGE_HTML = '''
<p style="color: {color}">
  {outcome}
</p>
'''


class EmailManager(object):
    def __init__(self, sender='todoit.manager@gmail.com'):
        self.sender = sender
        try:
            self.password = sys.argv[1]
        except IndexError:
            self.password = getpass.getpass('Enter Email Password: ')
        context = ssl.create_default_context()
        self.handler = smtplib.SMTP_SSL(
            host='smtp.gmail.com', port=465, context=context
        )
        self.message = MIMEMultipart('alternative')
        self.STATUS_CODES = [235, 250]

    def create_test_result_message(self, passing, message=''):
        self.message['Subject'] = 'Test Results'
        self.message['From'] = self.sender
        result = ('green', 'PASSING') if passing else ('red', 'FAILING')
        status = STATUS_MESSAGE_HTML.format(color=result[0], outcome=result[1])
        html = TEST_MESSAGE_HTML.format(status=status, message=message)
        self.message.attach(MIMEText(message, 'plain'))
        self.message.attach(MIMEText(html, 'html'))

    def send_email(self, recepient):
        connection = self.handler.ehlo()
        if connection[0] in self.STATUS_CODES:
            login = self.handler.login(self.sender, self.password)
            if login[0] in self.STATUS_CODES:
                self.message['To'] = recepient
                self.handler.sendmail(
                    self.sender, recepient, self.message.as_string()
                )
                self.handler.quit()


if __name__ == '__main__':
    gmail_obj = EmailManager()
    message = 'Test message'
    gmail_obj.create_message(subject='Testing', message=message)
    gmail_obj.send_email(recepient='elvisrodriguez1992@gmail.com')
