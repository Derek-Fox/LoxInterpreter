import sys
import app.Lox as Lox
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

def parseCmd(args):
    cmd = args[1]
    match cmd:
        case 'interactive':
            runInteractive()
        case 'tokenize':
            error = runTokenize(args[2])
            if error: sys.exit(65)
        case 'testPrint':
            testAstPrinter()
        case _:
            print(f'Unknown command: {cmd}', file=sys.stderr)
            exit(1)

def main():
    if len(sys.argv) < 2:
        print('Usage: ./your_program.sh <command> [filename]', file=sys.stderr)
        exit(1)
    else:
        parseCmd(sys.argv)


if __name__ == '__main__':
    main()
