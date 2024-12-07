from LoxClass import LoxClass

class LoxInstance:
    def __init__(self, l_class: LoxClass):
        self.l_class = l_class

    def __repr__(self):
        return f'<class {self.l_class.name} instance>'