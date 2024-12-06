from abc import ABC, abstractmethod
from Interpreter import Interpreter


class LoxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        """Return the number of arguments the LoxCallable expects."""
        pass

    @abstractmethod
    def call(self, interpreter: Interpreter, arguments: list[object]) -> object:
        """Call the LoxCallable with the given arguments. Uses the global environment of the passed interpreter."""
        pass
