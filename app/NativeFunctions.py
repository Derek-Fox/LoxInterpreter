from LoxCallable import LoxCallable
from LoxRuntimeError import LoxRuntimeError


class ReadInput(LoxCallable):
    name = 'readInput'

    def arity(self) -> int:
        return 0

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        return input()

    def __repr__(self):
        return '<native fn readInput>'


class Clock(LoxCallable):
    name = 'clock'

    def arity(self) -> int:
        return 0

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        import time
        return time.time()

    def __repr__(self):
        return '<native fn clock>'


class Sleep(LoxCallable):
    name = 'sleep'

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
    name = 'typeConvert'

    def arity(self) -> int:
        return 2

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        to_convert, target_type = arguments[0], arguments[1]

        try:
            if target_type == 'number':
                return float(to_convert)
            elif target_type == 'string':
                return interpreter.stringify(to_convert)
            elif target_type == 'boolean':
                if isinstance(to_convert, str) and to_convert.lower() == 'false':
                    return False  # convert str 'false' (with any caps) to boolean false, b/c is_truthy won't do that!
                return interpreter.is_truthy(to_convert)
            else:
                raise LoxRuntimeError(message=f"Invalid target type '{target_type}'.")
        except ValueError:
            raise LoxRuntimeError(
                message=f"Cannot convert '{'nil' if not to_convert else to_convert}' to '{target_type}'.")
