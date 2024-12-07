from LoxCallable import LoxCallable
from LoxFunction import LoxFunction

class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: dict[str, LoxFunction]):
        self.name = name
        self.methods = methods

    def find_method(self, name: str) -> LoxFunction | None:
        return self.methods.get(name)

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        from LoxInstance import LoxInstance
        instance = LoxInstance(self)
        return instance

    def arity(self) -> int:
        return 0

    def __repr__(self) -> str:
        return f'<class {self.name}>'
