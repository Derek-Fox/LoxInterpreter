import sys
import Lox as Lox
from Token import Token
from TokenType import TokenType
from AstPrinter import AstPrinter
from Expr import *


def testAstPrinter():
    expression = Binary(
        left=Unary(
            op=Token(TokenType.MINUS, "-", None, 1),
            right=Literal(123)),
        op=Token(TokenType.STAR, "*", None, 1),
        right=Grouping(
            expr=Literal(45.67)))

    print(AstPrinter().print(expression))


def runInteractive():
    Lox.runPrompt()


def runTokenize(file) -> bool:
    Lox.runFile(file)
    return Lox.hadError()


def displayHelp():
    print(
        '''
        Usage: python ./app/main.py <command> [filename]
        Available commands:
        - interactive: Run the interpreter in interactive mode
        - tokenize: Run the interpreter on the given file
        - test-print: Run the AstPrinter test
        - help: Display this help message''',
        file=sys.stderr
    )


def parseCmd(args):
    cmd = args[1]
    match cmd:
        case 'interactive':
            runInteractive()
        case 'tokenize':
            error = runTokenize(args[2])
            if error: sys.exit(65)
        case 'test-print':
            testAstPrinter()
        case 'help':
            displayHelp()
        case _:
            print(f'Unknown command: {cmd}', file=sys.stderr)
            exit(1)


def main():
    if len(sys.argv) < 2:
        print('Usage: python ./app/main.py <command> [filename]', file=sys.stderr)
        exit(1)
    else:
        parseCmd(sys.argv)


if __name__ == '__main__':
    main()
