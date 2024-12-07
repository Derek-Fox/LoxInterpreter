from LoxCallable import LoxCallable


class LoxClass(LoxCallable):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<class {self.name}>'

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        from LoxInstance import LoxInstance
        instance = LoxInstance(self)
        return instance

    def arity(self) -> int:
        return 0
