from Token import Token


class LoxRuntimeError(RuntimeError):
    def __init__(self, token: Token = None, message: str = None):
        self.message = message
        self.token = token
