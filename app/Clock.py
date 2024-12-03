from LoxCallable import LoxCallable
from Interpreter import Interpreter


class Clock(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter: Interpreter, arguments: list[object]) -> object:
        import time
        return time.time()

    def __repr__(self):
        return '<native fn>'
