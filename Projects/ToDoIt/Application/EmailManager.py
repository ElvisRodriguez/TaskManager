from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
import smtplib
import ssl
import sys


class EmailManager(object):
    def __init__(self, sender='todoit.manager@gmail.com'):
        self.sender = sender
        self.password = None
        with open('passwords.txt', 'r') as file:
            self.password = file.readline()[:-1]
        context = ssl.create_default_context()
        self.handler = smtplib.SMTP_SSL(
            host='smtp.gmail.com', port=465, context=context
        )
        self.message = MIMEMultipart('alternative')
        self.STATUS_CODES = [235, 250]

    def create_message(self, subject='', message=''):
        self.message['Subject'] = subject
        self.message['From'] = self.sender
        html = '''
            <html>
              <body>
                <b><i>
                  {message}
                </i></b>
              </body>
            </html>
        '''.format(message=message)
        self.message.attach(MIMEText(message, 'plain'))
        self.message.attach(MIMEText(html, 'html'))

    def send_email(self, recepient):
        if self.message is None:
            print('Message not created yet')
            return
        connection = self.handler.ehlo()
        if connection[0] in self.STATUS_CODES:
            print('Connection Status: OK')
            login = self.handler.login(self.sender, self.password)
            if login[0] in self.STATUS_CODES:
                self.message['To'] = recepient
                print('Login Successful')
                self.handler.sendmail(
                    self.sender, recepient, self.message.as_string()
                )
                print('Email sent, closing connection...')
                self.handler.quit()


if __name__ == '__main__':
    gmail_obj = EmailManager()
    message = 'Test message'
    gmail_obj.create_message(subject='Testing', message=message)
    gmail_obj.send_email(recepient='elvisrodriguez1992@gmail.com')
