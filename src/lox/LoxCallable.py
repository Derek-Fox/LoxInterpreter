from abc import ABC, abstractmethod

class LoxCallable(ABC):
    name = "Base LoxCallable"

    @abstractmethod
    def arity(self) -> int:
        """Return the number of arguments the LoxCallable expects."""
        pass

    @abstractmethod
    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        """Call the LoxCallable with the given arguments. Uses the global environment of the passed interpreter."""
        pass

    def check_arg_types(self, arg: str, *types: type[float | bool | str | list]):
        type_map = {
            float: "number",
            bool: "boolean",
            str: "string",
            list: "list"
        }

        from lox.LoxRuntimeError import LoxRuntimeError
        if not isinstance(arg, types):
            raise LoxRuntimeError(message=f"Need arguments of type {[type_map[t] for t in types]} for {self.name}.")