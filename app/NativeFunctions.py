from LoxCallable import LoxCallable
from LoxRuntimeError import LoxRuntimeError


class ReadInput(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        return input()

    def __repr__(self):
        return '<native fn readInput>'


class Clock(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        import time
        return time.time()

    def __repr__(self):
        return '<native fn clock>'


class Sleep(LoxCallable):
    def arity(self) -> int:
        return 1

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        import time

        sleep_time = arguments[0]

        if not isinstance(sleep_time, float):
            raise LoxRuntimeError(message="Need argument of type number for sleep().")

        time.sleep(float(sleep_time))
        return None


class TypeConvert(LoxCallable):
    def arity(self) -> int:
        return 2

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        to_convert, target_type = arguments[0], arguments[1]

        match target_type:
            case 'number':
                if to_convert:
                    return float(to_convert)
            case 'string':
                return interpreter.stringify(to_convert)
            case 'boolean':
                return interpreter.is_truthy(to_convert)
            case _:
                raise LoxRuntimeError(message=f"Invalid target type '{target_type}'.")

        raise LoxRuntimeError(message=f"Cannot convert '{'nil' if not to_convert else to_convert}' to '{target_type}'.")

