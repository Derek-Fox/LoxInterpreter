import TokenType as TokenType


class Token:
    def __init__(self, t_type: TokenType, lexeme: str, literal: object, line: int):
        self.t_type = t_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f'{self.t_type} {self.lexeme} {"null" if self.literal is None else self.literal}'