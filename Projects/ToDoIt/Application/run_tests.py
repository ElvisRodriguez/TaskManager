import datetime
import os


def wipe_test_file(filename):
    os.chdir(os.getcwd())
    current_date = str(datetime.datetime.date(datetime.datetime.now()))
    with open(filename, 'w') as file:
        file.write('Tests Results as of {date}:\n'.format(date=current_date))


def find_test_files():
    test_files = []
    os.chdir(os.getcwd())
    for filename in os.listdir():
        if '_test.py' in filename:
            test_files.append(filename)
    return test_files


def add_test_results_to_file(filename, test_files):
    for test_file in test_files:
        with open(filename, 'a') as file:
            file.write('{file} results:\n'.format(file=test_file))
        os.system('python3 {file}'.format(file=test_file))


def remove_non_text_from_file(filename):
    lines = []
    with open(filename, 'r') as file:
        lines.extend(
            [line for line in file.readlines() if line != line.lower()]
        )
    with open(filename, 'w') as file:
        for line in lines:
            if 'results' in line:
                file.write('*' * 50 + '\n')
                file.write(line)
            elif 'OK' in line:
                file.write(line)
                file.write('*' * 50 + '\n')
            else:
                file.write(line)
            file.write('\n')


if __name__ == '__main__':
    filename = 'test_output.txt'
    wipe_test_file(filename)
    test_files = find_test_files()
    add_test_results_to_file(filename, test_files)
    remove_non_text_from_file(filename)
