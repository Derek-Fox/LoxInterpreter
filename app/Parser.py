from Token import Token, TokenType as TT
from Expr import *
from Stmt import *


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    class ParseError(RuntimeError):
        pass

    def parse(self) -> list[Stmt]:
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())

        return statements

    # ---------- Methods for CFG productions -------------
    # No doc comments because they would get very repetitive.
    # Basically, each method corresponds to a production in the Context-Free Grammar
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

    # ----------- Helper methods ---------------
    def match(self, t_types: list[TT]) -> bool:
        """
        Advance if current Token is one of t_types.
        :param t_types: TokenTypes to check for.
        :return: True if match found, else false
        """
        for t_type in t_types:
            if self.check(t_type):
                self.advance()
                return True
        return False

    def check(self, t_type: TT):
        """
        Check if current token is of TokenType t_type
        :param t_type: TokenType to check for
        :return: True if types match, else false
        """
        if self.is_at_end(): return False
        return self.peek().t_type == t_type

    def peek(self) -> Token:
        """
        Get the current token. Do not advance/consume.
        :return: Token at current
        """
        return self.tokens[self.current]

    def is_at_end(self) -> bool:
        """
        Check if parser hit end of file.
        :return: True if at EOF token, else False
        """
        return self.peek().t_type == TT.EOF

    def previous(self) -> Token:
        """
        Get Token at current - 1
        :return: Token at current - 1
        """
        return self.tokens[self.current - 1]

    def advance(self) -> Token:
        """
        Get current Token and advance current pointer.
        :return: Token at current
        """
        if not self.is_at_end(): self.current += 1
        return self.previous()

    def consume(self, t_type: TT, err_message: str) -> Token:
        """
        Advance to next token if current token matches t_type, and return current
        :param t_type: TokenType to match at current
        :param err_message: Error message to raise if no match
        :return: current Token
        :raises: ParseError if current token doesn't match t_type
        """
        if self.check(t_type): return self.advance()
        raise self.error(self.peek(), err_message)

    def error(self, token: Token, message: str) -> ParseError:
        """
        Generate an error and alert Lox
        :param token: Token where error occurred
        :param message: Error message
        :return: ParseError to raise
        """
        from Lox import Lox
        Lox.error_token(token, message)
        return self.ParseError()

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().t_type == TT.SEMICOLON: return
            while self.peek().type in {TT.CLASS, TT.FUN, TT.VAR, TT.FOR, TT.IF, TT.WHILE, TT.PRINT, TT.RETURN}:
                return
            self.advance()

    def statement(self) -> Stmt:
        """
        Parse a statement from source.
        Matches the type of statement and calls the appropriate function.
        :return: Stmt object
        """
        if self.match([TT.PRINT]): return self.print_statement()

        return self.expression_statement()

    def print_statement(self) -> Stmt:
        """
        Parse a print statement.
        :return: Stmt object
        """
        value = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expression_statement(self) -> Stmt:
        """
        Parse an expression statement..
        :return: Stmt object
        """
        expr = self.expression()
        consume(TT.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)
