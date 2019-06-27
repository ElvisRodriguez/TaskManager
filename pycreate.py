import os
import sys


def create_test_file(filename):
    script = '{filename}_test.py'.format(filename=filename)
    os.chdir(os.getcwd())
    with open(script, 'w') as new_file:
        new_file.write('import collections\n')
        new_file.write('import sys\n\n\n')
        new_file.write('\nclass {filename}(object):\n'.format(
            filename=filename.title()))
        new_file.write('\tpass\n\n\n')
        new_file.write('if __name__ == \'__main__\':\n')
        new_file.write('\tprint(sys.argv[0])')
        new_file.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            create_test_file(sys.argv[i])
    else:
        print('Script filenames not given')
