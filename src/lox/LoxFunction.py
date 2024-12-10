from lox.LoxStmt import FunctionStmt
from lox.LoxCallable import LoxCallable
from lox.LoxEnvironment import Environment
from lox.LoxReturn import LoxReturn


class LoxFunction(LoxCallable):
    def __init__(self, declaration: FunctionStmt, closure: Environment, is_initializer: bool = False):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def arity(self) -> int:
        return len(self.declaration.params)

    def bind(self, instance: "LoxInstance"):
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration, environment, self.is_initializer)

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        from run.Interpreter import Interpreter
        environment = Environment(self.closure)

        for param, arg in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, arg)

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except LoxReturn as return_value:
            if self.is_initializer: return self.closure.get_at(0, "this")

            return return_value.value

        if self.is_initializer: return self.closure.get_at(0, "this")

    def __repr__(self):
        return f'<fn {self.declaration.name.lexeme}>'
