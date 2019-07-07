import os
import sys

def create_test_file(filename):
    test_file = '{filename}_test.py'.format(filename=filename)
    os.chdir(os.getcwd())
    with open(test_file, 'w') as new_file:
        new_file.write('import random\n')
        new_file.write('import unittest\n\n')
        new_file.write('import {filename}\n\n'.format(filename=filename))
        new_file.write(
            '\nclass Test{filename}(unittest.TestCase()):\n'.format(
                filename=filename.title()))
        new_file.write('\tpass\n\n\n')
        new_file.write('if __name__ == \'__main__\':\n')
        new_file.write('\tunittest.main()')
        new_file.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            create_test_file(sys.argv[i])
    else:
        print('Test filenames not given')
