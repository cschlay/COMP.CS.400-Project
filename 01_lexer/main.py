"""
The CLI program to perform lexical analysis with PLY for Principles of Programming Languages
course project.
"""

import codecs


def read_file(filename: str) -> str:
    """
    Reads the file data to string.

    Another code snippet given from instructions.
    :return: The file content as string.
    """
    with codecs.open(filename, 'r', encoding='utf-8') as INFILE:
        return INFILE.read()


def tokenize_file(filename: str):
    """
    Reads the data from file to string.
    I have moved the reading from example to this function so that tests can be run without CLI.

    :param filename: File to read.
    """
    file_data: str = read_file(filename=filename)
    print(file_data)


if __name__ == '__main__':
    """
    The initial CLI implementation is taken from example given at
    https://course-gitlab.tuni.fi/compcs400-principles-of-programming-languages_2020-2021/public_examples/-/blob/master/roman-numerals/tokenizer.py

    I think it was said in lectures that this part can be copied.
    """
    import argparse

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    group.add_argument('-f', '--file', help='filename to process')

    ns = parser.parse_args()
    if ns.who:
        # identify who wrote this
        print('424562 Chi-Hao Lay')
    elif ns.file is None:
        # user didn't provide input filename
        parser.print_help()
    else:
        tokenize_file(filename=ns.file)
