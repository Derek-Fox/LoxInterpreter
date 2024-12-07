class LoxReturn(RuntimeError):
    def __init__(self, value):
        self.value = value