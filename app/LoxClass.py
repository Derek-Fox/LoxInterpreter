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

        initializer = self.find_method("init")
        if initializer:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    def arity(self) -> int:
        initializer = self.find_method("init")
        return 0 if not initializer else initializer.arity()

    def __repr__(self) -> str:
        return f'<class {self.name}>'
