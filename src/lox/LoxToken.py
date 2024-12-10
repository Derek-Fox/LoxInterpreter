from enum import Enum, auto


class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = auto()  # (
    RIGHT_PAREN = auto()  # )
    LEFT_BRACE = auto()  # {
    RIGHT_BRACE = auto()  # }
    LEFT_BRACKET = auto()  # [
    RIGHT_BRACKET = auto()  # ]
    COMMA = auto()  # ,
    DOT = auto()  # .
    SEMICOLON = auto()  # ;
    CARAT = auto()  # ^

    # One or two character tokens.
    BANG = auto()  # !
    BANG_EQUAL = auto()  # !=
    EQUAL = auto()  # =
    EQUAL_EQUAL = auto()  # ==
    GREATER = auto()  # >
    GREATER_EQUAL = auto()  # >=
    LESS = auto()  # <
    LESS_EQUAL = auto()  # <=
    PLUS = auto()  # +
    PLUS_EQUAL = auto()  # +=
    PLUS_PLUS = auto()  # ++
    MINUS = auto()  # -
    MINUS_EQUAL = auto()  # -=
    MINUS_MINUS = auto()  # --
    SLASH = auto()  # /
    SLASH_EQUAL = auto()  # /=
    STAR = auto()  # *
    STAR_EQUAL = auto()  # *=

    # Literals.
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords.
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()

    def __str__(self):
        return self.name


class LoxToken:
    def __init__(self, t_type: TokenType, lexeme: str, literal: object, line: int):
        self.t_type = t_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f'{self.t_type} {self.lexeme} {"nil" if self.literal is None else self.literal}'