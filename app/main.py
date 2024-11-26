import sys
from Lox import Lox
from Token import Token, TokenType as TT
from AstPrinter import AstPrinter
from RpnPrinter import RpnPrinter
from Expr import *


def testRpnPrinter():
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


def testAstPrinter():
    expression = Binary(
        left=Unary(
            op=Token(TT.MINUS, "-", None, 1),
            right=Literal(123)),
        op=Token(TT.STAR, "*", None, 1),
        right=Literal(45.67))

    print(AstPrinter().print(expression))


def runInteractive():
    Lox.runPrompt()


def runTokenize(file) -> bool:
    Lox.runFile(file)
    return Lox.errored


def displayHelp():
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


def displayError(message: str):
    print(f'Error: {message}', file=sys.stderr)


def parseCmd(args):
    commands = {
        'interactive': runInteractive,
        'tokenize': lambda: runTokenize(args[2]),
        'test-AstPrint': testAstPrinter,
        'test-RpnPrint': testRpnPrinter,
        'help': displayHelp
    }

    cmd = args[1]
    func = commands.get(cmd)

    if not func:
        displayError(f'Unknown command {cmd}')
        sys.exit(1)

    error = func()
    if error: sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print('Usage: python ./app/main.py <command> [filename]', file=sys.stderr)
        exit(1)
    else:
        parseCmd(sys.argv)


if __name__ == '__main__':
    main()
