#!/home/elvisrodriguez1992/anaconda3/bin/python
import EmailManager
import TestManager


if __name__ == '__main__':
    test_manager = TestManager.TestManager()
    email_manager = EmailManager.EmailManager()
    test_manager.wipe_test_file()
    test_manager.add_test_results_to_file()
    test_manager.remove_non_text_from_file()
    all_tests_passing = test_manager.determine_if_all_tests_passing()
    message = []
    with open(test_manager.filename, 'r') as file:
        message = '<br>'.join(file.readlines())
    email_manager.create_test_result_message(
        passing=all_tests_passing, message=message
    )
    email_manager.send_email(recepient='elvisrodriguez1992@gmail.com')
