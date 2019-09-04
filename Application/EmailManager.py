'''
Sends emails on behalf of ToDoIt web application to both admins and users.
'''
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import getpass
import os
import smtplib
import ssl
import sys


STYLE = '''
style="font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif;
       font-size: 16px;
       line-height: 1.5em;
       padding-left: 25px;
       padding-right: 25px;
       text-align: left;"
'''


TEST_MESSAGE_HTML = '''
<html>
  <body>
    <div {style}>
      {status}
      <p>
        {message}
      </p>
    </div>
  </body>
</html>
'''

STATUS_MESSAGE_HTML = '''
<p style="color: {color}">
  {outcome}
</p>
'''


PASSWORD_RESET_HTML = '''
<html>
  <body>
    <div {style}>
    <p> Dear {username}, </p>
    <p>
    To reset your password <a href="{url}"> click here </a>.
    </p>
    <p>
        Alternatively, paste the following link in your browser's address bar:
    </p>
    <p> {url} </p>
    <p>
        If you have not requested a password reset simply ignore this message.
    </p>
    <p>Sincerely,</p>
    <p>The ToDoIt Team</p>
    </div>
  </body>
</html>
'''


TASK_NOTIFICATION_HTML = '''
<html>
  <body>
    <div {style}>
      <p> Hello {username}, </p>
      <p> It's time for your task/reminder: </p>
      <div style="border-bottom: 1px solid black"></div>
      <p><i> {task} </i></p>
    </div>
  </body>
</html>
'''


class EmailManager(object):
    '''Emails tests results to admin and password resets/pending tasks to users.
    '''

    def __init__(self, sender='todoit.manager@gmail.com', password=None):
        '''Initializes smtplib email handler.

        Args:
            sender (str): Email of application, generally not an argument that
                    should be changed from the default.
            password (str): Password of sender, can be passed in the
                            constructor, provided as a command line argument, or
                            given as input when prompted.

        Returns:
            None.
        '''
        self.sender = sender
        try:
            self.password = sys.argv[1]
        except IndexError:
            if password:
                self.password = password
            else:
                self.password = getpass.getpass('Enter Email Password: ')
        context = ssl.create_default_context()
        self.handler = smtplib.SMTP_SSL(
            host='smtp.gmail.com', port=465, context=context
        )
        self.message = MIMEMultipart('alternative')
        self.message['From'] = self.sender
        self.STATUS_CODES = [235, 250]

    def create_password_reset_message(self, username, url):
        '''Formats an email with instructions for a password reset.

        Args:
            username (str): Username of user requesting a password reset.
            url (str): URL of application's password reset page.

        Returns:
            None.
        '''
        self.message['Subject'] = 'Password Reset'
        html = PASSWORD_RESET_HTML.format(
            style=STYLE, username=username, url=url
        )
        self.message.attach(MIMEText(html, 'html'))

    def create_task_notification_message(self, username, task):
        '''Formats an email with a user's task.

        Args:
            username (str): Username of user with pending task.
            task (str): User's task/reminder.

        Returns:
            None.
        '''
        self.message['Subject'] = 'Task/Reminder Notification'
        html = TASK_NOTIFICATION_HTML.format(
            style=STYLE, username=username, task=task
        )
        self.message.attach(MIMEText(html, 'html'))

    def create_test_result_message(self, passing, message):
        '''Formats an email with the results of application's unit tests.

        Args:
            passing (bool): True if all unit tests are passing, false otherwise.
            message (str): Message containing output of unit tests.

        Returns:
            None.
        '''
        self.message['Subject'] = 'Test Results'
        result = ('green', 'PASSING') if passing else ('red', 'FAILING')
        status = STATUS_MESSAGE_HTML.format(color=result[0], outcome=result[1])
        html = TEST_MESSAGE_HTML.format(
            style=STYLE, status=status, message=message
        )
        self.message.attach(MIMEText(message, 'plain'))
        self.message.attach(MIMEText(html, 'html'))

    def send_email(self, recepient):
        '''Sends preformatted email to recepient.

        Args:
            recepient (str): Email of the intended recepient.

        Returns:
            None.
        '''
        connection = self.handler.ehlo()
        if connection[0] in self.STATUS_CODES:
            login = self.handler.login(self.sender, self.password)
            if login[0] in self.STATUS_CODES:
                self.message['To'] = recepient
                self.handler.sendmail(
                    self.sender, recepient, self.message.as_string()
                )
                self.handler.quit()
