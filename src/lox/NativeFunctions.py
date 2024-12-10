from lox.LoxCallable import LoxCallable
from lox.LoxRuntimeError import LoxRuntimeError
from abc import ABC
import random
import math

loxtype_to_pythontype = {
    "number": float,
    "boolean": bool,
    "string": str,
    "list": list
}

pythontype_to_loxtype = {
    float: "number",
    bool: "boolean",
    str: "string",
    list: "list"
}

"""
Ideas for more builtins:
Here are some ideas for additional native functions you could implement:
Trigonometric Functions: Functions like sin, cos, tan, asin, acos, and atan to perform trigonometric calculations.
String Manipulation: Functions like substring, toUpperCase, toLowerCase, trim, replace, and split.
List Operations: Functions like append, remove, indexOf, sort, and reverse.
File I/O: Functions to read from and write to files.
Error Handling: Functions to throw and catch custom errors.
"""


class NativeFunction(LoxCallable, ABC):
    """
    Base Native Function class.
    """
    name = "base nativefn"

    def __repr__(self):
        return f'<native fn {self.name}>'

    def check_arg_types(self, arg: object, *types: type[float | bool | str | list]):
        from lox.LoxRuntimeError import LoxRuntimeError
        if not isinstance(arg, types):
            raise LoxRuntimeError(
                message=f"Need arguments of type {[pythontype_to_loxtype[t] for t in types]} for {self.name}.")


class Print(NativeFunction):
    """
    Native function to print to stdout.
    """

    name = "print"

    def arity(self) -> int:
        return 1

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        print(interpreter.stringify(arguments[0]))
        return None

class TypeCheck(NativeFunction):
    """
    Native function to check the type of a value.
    """

    name = "isType"

    def arity(self) -> int:
        return 2

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        thing, want_type = arguments[0], arguments[1]

        self.check_arg_types(want_type, str)

        valid = ["number", "boolean", "string", "list"]
        if want_type not in valid:
            raise LoxRuntimeError(message=f"Invalid type '{want_type}' passed to isType. Must be one of {valid}.")

        return isinstance(thing, loxtype_to_pythontype[want_type])


class TypeConvert(NativeFunction):
    """
    Native function to convert a value to a different type. (number, string, boolean)
    """
    name = 'convert'

    def arity(self) -> int:
        return 2

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        to_convert, target_type = arguments[0], arguments[1]

        self.check_arg_types(target_type, str)

        valid = ["number", "boolean", "string"]
        if target_type not in valid:
            raise LoxRuntimeError(message=f"Invalid type '{type}' passed to isType. Must be one of {valid}.")

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
                raise LoxRuntimeError(
                    message=f"Invalid target type '{target_type}' for convert. Must be one of {valid}.")
        except ValueError:
            raise LoxRuntimeError(
                message=f"Cannot convert '{'nil' if not to_convert else to_convert}' to '{target_type}'.")


class SquareRoot(NativeFunction):
    """
    Native function to get the square root of a number.
    """

    name = "sqrt"

    def arity(self) -> int:
        return 1

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        num = arguments[0]

        self.check_arg_types(num, float)

        from math import sqrt
        return sqrt(num)


class NaturalLog(NativeFunction):
    """
    Native function to find the natural logarithm of a number.
    """

    name = "ln"

    def arity(self) -> int:
        return 1

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        num = arguments[0]

        self.check_arg_types(num, float)

        from math import log
        return log(num)


class Log10(NativeFunction):
    """
    Native function to find the base 10 logarithm of a number.
    """

    name = "log10"

    def arity(self) -> int:
        return 1

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        num = arguments[0]

        self.check_arg_types(num, float)

        from math import log10
        return log10(num)


class Exponential(NativeFunction):
    """
    Native function to calculate the exponential of a number.
    """

    name = "exp"

    def arity(self) -> int:
        return 1

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        num = arguments[0]

        self.check_arg_types(num, float)

        from math import exp
        return exp(num)


class RandomFloat(NativeFunction):
    """
    Native function to generate a random floating point number between two numbers.
    """
    name = "randFloat"

    def arity(self) -> int:
        return 2

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        bottom, top = arguments[0], arguments[1]

        self.check_arg_types(bottom, float)
        self.check_arg_types(top, float)

        bottom, top = map(float, (bottom, top))

        from random import uniform
        return uniform(bottom, top)


class RandomInt(NativeFunction):
    """
    Native function to generate a random int within a range.
    """

    name = "randInt"

    def arity(self) -> int:
        return 2

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        bottom, top = arguments[0], arguments[1]

        self.check_arg_types(bottom, float)
        self.check_arg_types(top, float)

        from random import randint
        return float(randint(int(bottom), int(top)))


class Length(NativeFunction):
    """
    Native function to get the length of a list or string.
    """
    name = "length"

    def arity(self) -> int:
        return 1

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        arg = arguments[0]

        self.check_arg_types(arg, list, str)

        return len(arg)


class ReadInput(NativeFunction):
    """
    Native function to read input from the user.
    """
    name = 'input'

    def arity(self) -> int:
        return 0

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        return input()


class Clock(NativeFunction):
    """
    Native function to get the current time in seconds since the epoch.
    """
    name = 'clock'

    def arity(self) -> int:
        return 0

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        import time
        return time.time()


class Sleep(NativeFunction):
    """
    Native function to sleep for a given number of seconds.
    """
    name = 'sleep'

    def arity(self) -> int:
        return 1

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        sleep_time = arguments[0]

        self.check_arg_types(sleep_time, float)

        if sleep_time <= 0:
            raise LoxRuntimeError(message="Need positive number for sleep.")

        import time
        time.sleep(sleep_time)
        return None


class Exit(NativeFunction):
    """
    Native function to exit the program with a given exit code.
    """
    name = 'exit'

    def arity(self) -> int:
        return 1

    def call(self, interpreter: "Interpreter", arguments: list[object]) -> object:
        exit_code = arguments[0]

        self.check_arg_types(exit_code, float)

        import sys
        sys.exit(int(exit_code))
