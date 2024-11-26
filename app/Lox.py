import sys
from Scanner import Scanner
from Token import Token, TokenType as TT
from Parser import Parser
from AstPrinter import AstPrinter
from RpnPrinter import RpnPrinter


class Lox:
    errored = False

    @classmethod
    def runFile(cls, filename: str):
        with open(filename) as file:
            file_contents = file.read()
        cls.run(file_contents)

    @classmethod
    def runPrompt(cls):
        while True:
            print('> ', end='')
            try:
                line = input()
                cls.run(line)
                Lox.errored = False
            except EOFError:
                return

    @classmethod
    def run(cls, source: str):
        scanner = Scanner(source)
        tokens = scanner.scanTokens()

        parser = Parser(tokens)
        expr = parser.parse()

        if Lox.errored: return

        print(AstPrinter().print(expr))

    @classmethod
    def error(cls, token: Token, message: str):
        where = 'at end' if token.t_type == TT.EOF else f'at {token.lexeme}'
        cls.report(token.line, where, message)
        Lox.errored = True

    @classmethod
    def report(cls, line: int, where, message: str):
        print(f'[line {line}] Error {where}: {message}', file=sys.stderr)
