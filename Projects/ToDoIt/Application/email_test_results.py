#!/usr/bin/env python3
import EmailManager

from run_tests import *


def email_test_results():
    filename = 'test_output.txt'
    gmail_obj = EmailManager.EmailManager()
    wipe_test_file(filename)
    test_files = find_test_files()
    add_test_results_to_file(filename, test_files)
    remove_non_text_from_file(filename)
    all_tests_passing = determine_if_all_tests_passing(filename, test_files)
    message = []
    with open(filename, 'r') as file:
        message = '<br>'.join(file.readlines())
    gmail_obj.create_test_result_message(
        passing=all_tests_passing, message=message
    )
    gmail_obj.send_email(recepient='elvisrodriguez1992@gmail.com')


if __name__ == '__main__':
    email_test_results()
