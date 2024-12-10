from lox.LoxCallable import LoxCallable
from lox.LoxFunction import LoxFunction


class LoxClass(LoxCallable):
    def __init__(self, name: str, superclass: "LoxClass", methods: dict[str, LoxFunction]):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def find_method(self, name: str) -> LoxFunction | None:
        if name in self.methods:
            return self.methods[name]

        if self.superclass:
            return self.superclass.find_method(name)

        return None

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        from lox.LoxInstance import LoxInstance
        instance = LoxInstance(self)

        initializer = self.find_method("init")
        if initializer:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    def arity(self) -> int:
        initializer = self.find_method("init")
        return 0 if not initializer else initializer.arity()

    def check_arg_types(self, arg: str, *types: type[float | bool | str | list]):
        pass  # user needs to implement their own sanity checks if they want them

    def __repr__(self) -> str:
        return f'<class {self.name}>'
