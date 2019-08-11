import datetime
import os


BLOCK_SIZE = 80


class TestManager(object):
    def __init__(self, filename='test_output.txt'):
        self.filename = filename

    def __find_test_files(self):
        test_files = []
        os.chdir(os.getcwd())
        for filename in os.listdir():
            if '_test.py' in filename:
                test_files.append(filename)
        return test_files

    def wipe_test_file(self):
        os.chdir(os.getcwd())
        current_date = str(datetime.datetime.date(datetime.datetime.now()))
        with open(self.filename, 'w') as file:
            file.write(
                'Tests Results as of {date}:\n'.format(date=current_date)
            )

    def add_test_results_to_file(self):
        test_files = self.__find_test_files()
        for test_file in test_files:
            with open(self.filename, 'a') as file:
                file.write('{file} results:\n'.format(file=test_file))
            os.system('python3 {file}'.format(file=test_file))

    def determine_if_all_tests_passing(self):
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
    test_runner = TestManager()
    test_runner.wipe_test_file()
    test_runner.add_test_results_to_file()
    test_runner.remove_non_text_from_file()
