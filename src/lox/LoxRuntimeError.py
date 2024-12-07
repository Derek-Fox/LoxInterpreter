class LoxRuntimeError(RuntimeError):
    def __init__(self, token: "LoxToken" = None, message: str = None):
        self.token = token
        self.message = message
