import codecs

import ssparser


def read_file(filename: str):
    with codecs.open(filename, 'r', encoding='utf-8') as INFILE:
        return INFILE.read()


def parse_file(filename: str):
    file_data: str = read_file(filename=filename)
    ssparser.parse_data(data=file_data)


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
        print('424562 Chi-Hao Lay')
    elif ns.file is None:
        parser.print_help()
    else:
        parse_file(filename=ns.file)
