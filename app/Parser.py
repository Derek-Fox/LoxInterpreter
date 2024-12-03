from Expr import *
from Stmt import *
from Token import TokenType as TT


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    class ParseError(RuntimeError):
        pass

    def parse(self) -> list[Stmt]:
        """
        Parse the tokens.
        :return: List of statements
        """
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())

        return statements

    # ---------- Methods for CFG productions -------------
    # No doc comments because they would get very repetitive.
    # Basically, each method corresponds to a production in the Context-Free Grammar
    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.logic_or()

        if self.match([TT.EQUAL]):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, VariableExpr):
                name = expr.name
                return AssignExpr(name, value)

            self.error(equals, "Invalid assignment target.")

        return expr

    def logic_or(self) -> Expr:
        expr = self.logic_and()

        while self.match([TT.OR]):
            operator = self.previous()
            right = self.logic_and()
            expr = LogicalExpr(expr, operator, right)

        return expr

    def logic_and(self) -> Expr:
        expr = self.equality()

        while self.match([TT.AND]):
            operator = self.previous()
            right = self.equality()
            expr = LogicalExpr(expr, operator, right)

        return expr

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match([TT.BANG_EQUAL, TT.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match([TT.GREATER, TT.GREATER_EQUAL, TT.LESS, TT.LESS_EQUAL]):
            operator = self.previous()
            right = self.term()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match([TT.MINUS, TT.PLUS]):
            operator = self.previous()
            right = self.factor()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match([TT.SLASH, TT.STAR]):
            operator = self.previous()
            right = self.unary()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match([TT.BANG, TT.MINUS]):
            operator = self.previous()
            right = self.unary()
            return UnaryExpr(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match([TT.FALSE]): return LiteralExpr(False)
        if self.match([TT.TRUE]): return LiteralExpr(True)
        if self.match([TT.NIL]): return LiteralExpr(None)

        if self.match([TT.NUMBER, TT.STRING]): return LiteralExpr(self.previous().literal)

        if self.match([TT.IDENTIFIER]): return VariableExpr(self.previous())

        if self.match([TT.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TT.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpr(expr)

        raise self.error(self.peek(), "Expect expression.")

    def statement(self) -> Stmt:
        if self.match([TT.FOR]): return self.for_statement()
        if self.match([TT.IF]): return self.if_statement()
        if self.match([TT.PRINT]): return self.print_statement()
        if self.match([TT.WHILE]): return self.while_statement()
        if self.match([TT.LEFT_BRACE]): return BlockStmt(self.block())

        return self.expression_statement()

    def block(self) -> list[Stmt]:
        statements = []

        while not self.check(TT.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TT.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def for_statement(self) -> Stmt:
        self.consume(TT.LEFT_PAREN, "Expect '(' after 'for'.")

        if self.match([TT.SEMICOLON]):
            initializer = None
        elif self.match([TT.VAR]):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition = None
        if not self.check(TT.SEMICOLON):
            condition = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after 'for' condition.")

        increment = None
        if not self.check(TT.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TT.RIGHT_PAREN, "Expect ')' after 'for' clauses.")

        body = self.statement()

        # de-sugar the for loop syntax
        if increment:
            body = BlockStmt([body, ExpressionStmt(increment)])

        body = WhileStmt(condition if condition else LiteralExpr(True), body)

        if initializer:
            body = BlockStmt([initializer, body])

        return body

    def if_statement(self) -> Stmt:
        self.consume(TT.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TT.RIGHT_PAREN, "Expect ')' after 'if' condition.")

        thenBranch = self.statement()
        elseBranch = None

        if self.match([TT.ELSE]):
            elseBranch = self.statement()

        return IfStmt(condition, thenBranch, elseBranch)

    def while_statement(self) -> Stmt:
        self.consume(TT.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TT.RIGHT_PAREN, "Expect ')' after 'while' condition.")

        body = self.statement()

        return WhileStmt(condition, body)

    def print_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(value)

    def expression_statement(self) -> Stmt:
        expr = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStmt(expr)

    def declaration(self) -> Stmt | None:
        try:
            if self.match([TT.VAR]): return self.var_declaration()
            return self.statement()
        except Parser.ParseError:
            self.synchronize()
            return None

    def var_declaration(self) -> Stmt:
        name = self.consume(TT.IDENTIFIER, "Expect variable name.")

        initializer = None if not self.match([TT.EQUAL]) else self.expression()

        self.consume(TT.SEMICOLON, "Expect ';' after variable declaration.")
        return VarStmt(name, initializer)

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
        """
        Enter panic mode and try to synchronize the parser. Basically, skip to the next statement.
        """
        self.advance()

        while not self.is_at_end():
            if self.previous().t_type == TT.SEMICOLON: return
            while self.peek().t_type in {TT.CLASS, TT.FUN, TT.VAR, TT.FOR, TT.IF, TT.WHILE, TT.PRINT, TT.RETURN}:
                return
            self.advance()
