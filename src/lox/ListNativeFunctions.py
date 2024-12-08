from .LoxCallable import LoxCallable
from .LoxRuntimeError import LoxRuntimeError


class ListLen(LoxCallable):
    name = "length"

    def arity(self) -> int:
        return 1

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        lst = arguments[0]
        if not isinstance(lst, list):
            raise LoxRuntimeError(message="Need argument of type list.")

        return len(list(lst))

    def __repr__(self):
        return '<native fn length>'