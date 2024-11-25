import sys
from app.Scanner import Scanner


class LoxError:
    __had_error = False

    @classmethod
    def hadError(cls) -> bool:
        return cls.__had_error

    @classmethod
    def set(cls):
        cls.__had_error = True

    @classmethod
    def unset(cls):
        cls.__had_error = False


def runFile(filename: str):
    with open(filename) as file:
        file_contents = file.read()
    run(file_contents)


def runPrompt():
    while True:
        print('> ', end='')
        try:
            line = input()
            run(line)
            LoxError.unset()
        except EOFError:
            return


def run(source: str):
    scanner = Scanner(source)
    tokens = scanner.scanTokens()

    # For now, just print the tokens.
    for token in tokens:
        print(token)


def error(line: int, message: str):
    LoxError.set()
    report(line, '', message)


def report(line: int, where, message: str):
    print(f'[line {line}] Error{where}: {message}', file=sys.stderr)


def hadError() -> bool:
    return LoxError.hadError()
