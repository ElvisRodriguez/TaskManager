'''
Runs and logs all unit test results in Application.
'''
import datetime
import os
import time


BLOCK_SIZE = 80


class TestManager(object):
    '''Finds all python test modules and runs them, saving their output.
    '''

    def __init__(self, filename='test_output.txt'):
        '''Initializes object with filename of test output.

        Args:
            filename: filename where unit test results should be piped to.
                      Generally this argument should remain as the default.

        Returns:
            None.
        '''
        self.filename = filename

    def __find_test_files(self):
        '''Finds all python unit test modules in the current directory.

        Args:
            None.

        Returns:
            A list of all the python unit test files.
        '''
        test_files = []
        os.chdir(os.getcwd())
        for filename in os.listdir():
            if '_test.py' in filename:
                test_files.append(filename)
        return test_files

    def wipe_test_file(self):
        '''Opens self.filename and wipes it of previous test data.

        Args:
            None.

        Returns:
            None.
        '''
        os.chdir(os.getcwd())
        current_date = str(datetime.datetime.date(datetime.datetime.now()))
        with open(self.filename, 'w') as file:
            file.write(
                'Tests Results as of {date}:\n'.format(date=current_date)
            )

    def add_test_results_to_file(self):
        '''Runs every unit test file found and writes ouput to self.filename.

        Args:
            None.

        Returns:
            None.
        '''
        test_files = self.__find_test_files()
        for test_file in test_files:
            with open(self.filename, 'a') as file:
                file.write('{file} results:\n'.format(file=test_file))
            os.system('python {file}'.format(file=test_file))

    def determine_if_all_tests_passing(self):
        '''Checks if all unit tests have passing results.

        Args:
            None.

        Returns:
            True if all tests have the line 'OK\n', False otherwise.
        '''
        passing_tests = 0
        test_files = self.__find_test_files()
        number_of_tests = len(test_files)
        with open(self.filename, 'r') as file:
            for line in file.readlines():
                if line == 'OK\n':
                    passing_tests += 1
        if passing_tests == number_of_tests:
            return True
        return False

    def remove_non_text_from_file(self):
        '''Removes all unimportant text from test file output.

        Args:
            None.

        Returns:
            None.
        '''
        lines = []
        with open(self.filename, 'r') as file:
            lines.extend(
                [line for line in file.readlines() if line != line.lower()]
            )
        with open(self.filename, 'w') as file:
            for line in lines:
                if 'results' in line:
                    file.write('_' * BLOCK_SIZE + '\n')
                    file.write(line)
                elif 'OK' in line:
                    file.write(line)
                    file.write('_' * BLOCK_SIZE + '\n')
                else:
                    file.write(line)


if __name__ == '__main__':
    test_manager = TestManager()
    test_manager.wipe_test_file()
    test_manager.add_test_results_to_file()
    test_manager.remove_non_text_from_file()
