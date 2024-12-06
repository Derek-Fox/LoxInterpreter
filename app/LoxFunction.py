from Stmt import FunctionStmt
from LoxCallable import LoxCallable
from Interpreter import Interpreter
from Environment import Environment


class LoxFunction(LoxCallable):
    def __init__(self, declaration: FunctionStmt):
        self.declaration = declaration

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter: Interpreter, arguments: list[object]) -> object:
        environment = Environment(interpreter.globals)

        for param, arg in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, arg)

        interpreter.execute_block(self.declaration.body, environment)
        return None  # TODO: return values from functions

    def __repr__(self):
        return f'<fn {self.declaration.name.lexeme}>'
