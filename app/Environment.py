from Token import Token
from LoxRuntimeError import LoxRuntimeError

class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name: str, value: object):
        self.values[name] = value

    def get(self, name: Token) -> object:
        lexeme = name.lexeme
        if lexeme in self.values:
            return self.values[lexeme]

        raise LoxRuntimeError(name, f"Undefined variable '{lexeme}'.")