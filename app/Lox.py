import sys
from Scanner import Scanner
from Token import Token, TokenType as TT
from Parser import Parser
from AstPrinter import AstPrinter
from RpnPrinter import RpnPrinter

class LoxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str):
        self.message = message
        self.token = token

class Lox:
    had_error = False
    had_runtime_error = False

    @classmethod
    def run_file(cls, filename: str):
        """
        Run Lox code from file.
        :param filename: path to file
        """
        with open(filename) as file:
            file_contents = file.read()
        cls.run(file_contents)

    @classmethod
    def run_prompt(cls):
        """
        Run interactive Lox prompt.
        """
        while True:
            print('> ', end='')
            try:
                line = input()
                cls.run(line)
                Lox.had_error = False
            except EOFError:
                return

    @classmethod
    def run(cls, source: str):
        """
        Run scanner, parser, interpreter on source.
        :param source: String of Lox source code.
        """
        scanner = Scanner(source)
        tokens = scanner.scan()

        parser = Parser(tokens)
        expr = parser.parse()

        if Lox.had_error: return

        print(AstPrinter().print(expr))  # Currently, we just print the AST

    @classmethod
    def error(cls, token: Token, message: str):
        """
        Set error in Lox.
        :param token: Token where error occurred
        :param message: Error message
        """
        where = 'at end' if token.t_type == TT.EOF else f'at {token.lexeme}'
        cls.report(token.line, where, message)
        Lox.had_error = True

    @classmethod
    def report(cls, line: int, where, message: str):
        """
        Report error to the user.
        :param line: Line where error occurred
        :param where: Where in the line error occurred
        :param message: Error message
        """
        print(f'[line {line}] Error {where}: {message}', file=sys.stderr)

    @classmethod
    def runtime_error(cls, error: LoxRuntimeError):
        print(f'{error.message}\n[line {error.token.line}]')
        Lox.had_runtime_error = True
