import sys

from Interpreter import Interpreter
from Parser import Parser
from Resolver import Resolver
from Scanner import Scanner


class Lox:
    interpreter = Interpreter()
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

        if Lox.had_error: sys.exit(65)
        if Lox.had_runtime_error: sys.exit(70)

    @classmethod
    def run_prompt(cls):
        """
        Run interactive Lox prompt.
        """
        while True:
            print('> ', end='')
            try:
                line = input()
                cls.run(line, repl=True)
                Lox.had_error = False
            except EOFError:
                return

    @classmethod
    def run(cls, source: str, repl: bool = False):
        """
        Run scanner, parser, resolver, and interpreter on source.
        :param source: String of Lox source code.
        :param repl: Whether it is running in the repl.
        """
        # Scan
        scanner = Scanner(source)
        tokens = scanner.scan()

        # Parse
        parser = Parser(tokens)
        statements = parser.parse()
        if Lox.had_error: return  # stop if there are syntax (parse) errors

        # Resolve
        resolver = Resolver(Lox.interpreter)
        resolver.resolve_all(statements)
        if Lox.had_error: return  # stop if there are resolution errors

        # Interpret
        Lox.interpreter.interpret(statements, repl)

    @classmethod
    def error_line(cls, line: int, message: str):
        """
        Report error at given line to Lox
        :param line: Line where error occurred
        :param message: Error message
        """
        cls.report(line, "", message)

    @classmethod
    def error_token(cls, token: "LoxToken", message: str):
        """
        Report error at given token to Lox.
        :param token: Token where error occurred
        :param message: Error message
        """
        from lox.LoxToken import TokenType as TT
        where = 'at end' if token.t_type == TT.EOF else f"at '{token.lexeme}'"
        cls.report(token.line, where, message)

    @classmethod
    def report(cls, line: int, where: str, message: str):
        """
        Report error to the user.
        :param line: Line where error occurred
        :param where: Where in the line error occurred
        :param message: Error message
        """
        print(fr'[line {line}] Error {where}: {message}', file=sys.stderr)
        Lox.had_error = True

    @classmethod
    def runtime_error(cls, error: "LoxRuntimeError"):
        """
        Report runtime error to Lox.
        :param error: LoxRuntimeError
        """
        print(f'[line {error.token.line}] LoxRuntimeError: {error.message}', file=sys.stderr)
        Lox.had_runtime_error = True
