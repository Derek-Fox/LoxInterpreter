from LoxClass import LoxClass
from Token import Token
from LoxRuntimeError import LoxRuntimeError


class LoxInstance:
    def __init__(self, l_class: LoxClass):
        self.l_class = l_class
        self.fields = {}

    def get(self, name: "Token"):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.l_class.find_method(name.lexeme)
        if method: return method.bind(self)

        raise LoxRuntimeError(name, f"Undefined property {name.lexeme}.")

    def set(self, name: "Token", value: object):
        self.fields[name.lexeme] = value

    def __repr__(self):
        return f'<class {self.l_class.name} instance>'
