from Stmt import FunctionStmt
from LoxCallable import LoxCallable
from Environment import Environment
from Return import Return

class LoxFunction(LoxCallable):
    def __init__(self, declaration: FunctionStmt, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        from Interpreter import Interpreter
        environment = Environment(self.closure)

        for param, arg in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, arg)

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as returnValue:
            return returnValue.value

    def __repr__(self):
        return f'<fn {self.declaration.name.lexeme}>'
