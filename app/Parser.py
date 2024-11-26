from Token import Token, TokenType as TT
from Expr import *


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    class ParseError(RuntimeError):
        pass

    def parse(self) -> Expr | None:
        try:
            return self.expression()
        except self.ParseError:
            return None

    # methods for CFG rules
    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match([TT.BANG_EQUAL, TT.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match([TT.GREATER, TT.GREATER_EQUAL, TT.LESS, TT.LESS_EQUAL]):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match([TT.MINUS, TT.PLUS]):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match([TT.SLASH, TT.STAR]):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match([TT.BANG, TT.MINUS]):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match([TT.FALSE]): return Literal(False)
        if self.match([TT.TRUE]): return Literal(True)
        if self.match([TT.NIL]): return Literal(None)

        if self.match([TT.NUMBER, TT.STRING]): return Literal(self.previous().literal)

        if self.match([TT.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TT.RIGHT_PAREN, "Expected ')' after expression.")
            return Grouping(expr)

        raise self.error(self.peek(), "Expected expression.")

    # helper functions
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
        return self.tokens[self.current]

    def isAtEnd(self) -> bool:
        return self.peek().t_type == TT.EOF

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def advance(self) -> Token:
        if not self.isAtEnd(): self.current += 1
        return self.previous()

    def consume(self, t_type: TT, message: str) -> Token:
        if self.check(t_type): return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str) -> ParseError:
        from Lox import Lox
        Lox.error(token, message)
        return self.ParseError()

    def synchronize(self):
        self.advance()

        while not self.isAtEnd():
            if self.previous().t_type == TT.SEMICOLON: return
            if self.peek().type in {TT.CLASS, TT.FUN, TT.VAR, TT.FOR, TT.IF, TT.WHILE, TT.PRINT, TT.RETURN}:
                return
            self.advance()
