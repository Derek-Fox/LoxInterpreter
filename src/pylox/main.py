import sys
import argparse
from lox.Lox import Lox


def main():
    parser = argparse.ArgumentParser(description='Lox Interpreter written in Python.')
    parser.add_argument('filename', nargs='?',
                        help='Optional file to run as Lox source. Omit to run in interactive mode.')
    args = parser.parse_args()

    Lox.run_prompt() if not args.filename else Lox.run_file(args.filename)


if __name__ == '__main__':
    main()
