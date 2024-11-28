import sys
from Lox import Lox
from Token import Token, TokenType as TT
from AstPrinter import AstPrinter
from RpnPrinter import RpnPrinter
from Expr import *


def test_RpnPrinter():
    expression = Binary(
        left=Binary(
            left=Literal(9),
            op=Token(TT.MINUS, "-", None, 1),
            right=Literal(8)),
        op=Token(TT.STAR, "*", None, 1),
        right=Binary(
            left=Literal(5),
            op=Token(TT.PLUS, "+", None, 1),
            right=Literal(3)
        ))

    print(RpnPrinter().print(expression))


def test_AstPrinter():
    expression = Binary(
        left=Unary(
            op=Token(TT.MINUS, "-", None, 1),
            right=Literal(123)),
        op=Token(TT.STAR, "*", None, 1),
        right=Literal(45.67))

    print(AstPrinter().print(expression))


def run_interactive():
    Lox.run_prompt()


def run_tokenize(file) -> bool:
    Lox.run_file(file)
    return Lox.had_error


def display_help():
    print(
        '''
        Usage: python ./app/main.py <command> [filename]
        Available commands:
        - interactive: Run the interpreter in interactive mode
        - tokenize: Run the interpreter on the given file
        - test-AstPrint: Run the AstPrinter test
        - help: Display this help message''',
        file=sys.stderr
    )


def display_error(message: str):
    print(f'Error: {message}', file=sys.stderr)


def parse_cmd(args):
    commands = {
        'interactive': run_interactive,
        'tokenize': lambda: run_tokenize(args[2]),
        'test-AstPrint': test_AstPrinter,
        'test-RpnPrint': test_RpnPrinter,
        'help': display_help
    }

    cmd = args[1]
    func = commands.get(cmd)

    if not func:
        display_error(f'Unknown command {cmd}')
        sys.exit(1)

    error = func()
    if error: sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print('Usage: python ./app/main.py <command> [filename]', file=sys.stderr)
        exit(1)
    else:
        parse_cmd(sys.argv)


if __name__ == '__main__':
    main()
