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


PASSWORD_RESET_HTML = '''
<html>
  <body>
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
        self.message['From'] = self.sender
        html = PASSWORD_RESET_HTML.format(username=username, url=url)
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
        self.message['From'] = self.sender
        result = ('green', 'PASSING') if passing else ('red', 'FAILING')
        status = STATUS_MESSAGE_HTML.format(color=result[0], outcome=result[1])
        html = TEST_MESSAGE_HTML.format(status=status, message=message)
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
