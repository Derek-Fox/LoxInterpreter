from Token import Token
from LoxRuntimeError import LoxRuntimeError


class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name: str, value: object):
        """
        Define a variable in the environment.
        e.g. var a = 1;
        :param name: Variable's name
        :param value: Variable's value
        """
        self.values[name] = value

    def assign(self, name: Token, value: object):
        """
        Assign a variable a new value.
        e.g. a = 2; (Assuming a has been defined).
        :param name: Token to assign to
        :param value: Variable's value
        :raises: LoxRuntimeError if trying to assign to undefined variable
        """
        lexeme = name.lexeme
        if lexeme in self.values:
            self.values[lexeme] = value
            return

        raise LoxRuntimeError(name, f"Undefined variable '{lexeme}'.")

    def get(self, name: Token) -> object:
        """
        Get the value of a variable in the environment.
        :param name: Token of the variable
        :return: Value of the variable
        ":raises: LoxRuntimeError if trying to get value of undefined variable
        """
        lexeme = name.lexeme
        if lexeme in self.values:
            return self.values[lexeme]

        raise LoxRuntimeError(name, f"Undefined variable '{lexeme}'.")
