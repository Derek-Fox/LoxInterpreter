from Token import Token
from LoxRuntimeError import LoxRuntimeError


class Environment:
    def __init__(self, enclosing: "Environment" = None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name: str, value: object):
        """
        Define a variable in the environment.
        e.g. var a = 1;
        :param name: Variable's name
        :param value: Variable's value
        """
        self.values[name] = value

    def assign(self, name: Token, value: object):
        """
        Assign a variable a new value.
        e.g. a = 2; (Assuming a has been defined).
        :param name: Token to assign to
        :param value: Variable's value
        :raises: LoxRuntimeError if trying to assign to undefined variable
        """
        lexeme = name.lexeme
        if lexeme in self.values:
            self.values[lexeme] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, f"Undefined variable '{lexeme}'.")

    def get(self, name: Token) -> object:
        """
        Get the value of a variable in the environment.
        :param name: Token of the variable
        :return: Value of the variable
        ":raises: LoxRuntimeError if trying to get value of undefined variable
        """
        lexeme = name.lexeme
        if lexeme in self.values:
            return self.values[lexeme]

        if self.enclosing: return self.enclosing.get(name)

        raise LoxRuntimeError(name, f"Undefined variable '{lexeme}'.")

    def get_at(self, distance: int, name: str) -> object:
        """
        Get the value of a variable which is a certain depth in the environment hierarchy.
        :param distance: Depth of target variable in environment hierarchy
        :param name: Variable name (lexeme)
        :return: The variable's value
        """
        return self.ancestor(distance).values.get(name)

    def assign_at(self, distance: int, name: Token, value: object):
        """
        Assign a value to a variable which is a certain depth in the environment hierarchy.
        :param distance: Depth of target variable in environment hierarchy
        :param name: Variable name (lexeme)
        :param value: New value for the variable
        """
        self.ancestor(distance).values[name.lexeme] = value

    def ancestor(self, distance: int) -> "Environment":
        """
        Find the ancestor of the environment a given number of steps away.
        :param distance: Depth to walk in environment hierarchy
        :return: Ancestor environment
        """
        environment = self
        for _ in range(distance):
            environment = environment.enclosing

        return environment
