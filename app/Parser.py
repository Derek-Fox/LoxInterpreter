from TokenType import TokenType as TT
from Token import Token
from Expr import *


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match([TT.BANG_EQUAL, TT.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def match(self, t_types: list[TT]) -> bool:
        for t_type in t_types:
            if self.check(t_type):
                self.advance()
                return True
        return False

    def check(self, t_type: TT):
        if self.isAtEnd(): return False
        return self.peek().t_type == t_type

    def peek(self) -> Token:
        return self.tokens[current]
