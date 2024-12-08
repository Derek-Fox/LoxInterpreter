from lox.LoxExpr import *
from lox.LoxStmt import *
from lox.LoxToken import LoxToken, TokenType as TT


class Parser:
    MAX_FUNC_ARGS = 255

    def __init__(self, tokens: list[LoxToken]):
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
    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.logic_or()

        if self.match(TT.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, VariableExpr):
                return AssignExpr(expr.name, value)
            elif isinstance(expr, GetExpr):
                return SetExpr(expr.object, expr.name, value)
            elif isinstance(expr, AccessExpr):
                pass  # todo: support assigning to list at index

            self.error(equals, "Invalid assignment target.")

        return expr

    def logic_or(self) -> Expr:
        expr = self.logic_and()

        while self.match(TT.OR):
            operator = self.previous()
            right = self.logic_and()
            expr = LogicalExpr(expr, operator, right)

        return expr

    def logic_and(self) -> Expr:
        expr = self.equality()

        while self.match(TT.AND):
            operator = self.previous()
            right = self.equality()
            expr = LogicalExpr(expr, operator, right)

        return expr

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match(TT.BANG_EQUAL, TT.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match(TT.GREATER, TT.GREATER_EQUAL, TT.LESS, TT.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(TT.MINUS, TT.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(TT.SLASH, TT.STAR):
            operator = self.previous()
            right = self.unary()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match(TT.BANG, TT.MINUS):
            operator = self.previous()
            right = self.unary()
            return UnaryExpr(operator, right)

        return self.call()

    def primary(self) -> Expr:
        if self.match(TT.FALSE): return LiteralExpr(False)
        if self.match(TT.TRUE): return LiteralExpr(True)
        if self.match(TT.NIL): return LiteralExpr(None)
        if self.match(TT.NUMBER, TT.STRING): return LiteralExpr(self.previous().literal)
        if self.match(TT.THIS): return ThisExpr(self.previous())
        if self.match(TT.IDENTIFIER): return VariableExpr(self.previous())

        if self.match(TT.SUPER):
            keyword = self.previous()
            self.consume(TT.DOT, "Expect '.' after 'super'.")
            method = self.consume(TT.IDENTIFIER, "Expect superclass method name.")
            return SuperExpr(keyword, method)

        if self.match(TT.LEFT_PAREN):
            expr = self.expression()
            self.consume(TT.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpr(expr)

        if self.match(TT.LEFT_BRACKET):
            return self.list_expr()

        raise self.error(self.peek(), "Expect expression.")

    def call(self) -> Expr:
        expr = self.primary()

        while True:
            if self.match(TT.LEFT_PAREN):
                expr = self.finish_call(expr)
            elif self.match(TT.DOT):
                name = self.consume(TT.IDENTIFIER, "Expect property name after '.'.")
                expr = GetExpr(expr, name)
            elif self.match(TT.LEFT_BRACKET):
                return self.finish_access(expr)
            else:
                break

        return expr

    def finish_call(self, callee: Expr) -> CallExpr:
        arguments = []

        if not self.check(TT.RIGHT_PAREN):
            while True:
                if len(arguments) >= self.MAX_FUNC_ARGS:
                    self.error(self.peek(), f"Can't have more than {self.MAX_FUNC_ARGS} arguments")
                arguments.append(self.expression())
                if not self.match(TT.COMMA): break

        paren = self.consume(TT.RIGHT_PAREN, "Expect ')' after arguments.")

        return CallExpr(callee, paren, arguments)

    def finish_access(self, lst: Expr) -> AccessExpr:
        idx = None
        if self.match(TT.NUMBER):
            idx = LiteralExpr(self.previous().literal)
        elif self.match(TT.IDENTIFIER):
            idx = VariableExpr(self.previous())
        else:
            idx = self.term()

        self.consume(TT.RIGHT_BRACKET, "Expect ']' after index.")

        return AccessExpr(lst, idx)

    def list_expr(self) -> ListExpr:
        items = []

        if self.match(TT.RIGHT_BRACKET):  # empty list
            return ListExpr(items)

        while not self.is_at_end():  # 1 or more items
            items.append(self.logic_or())
            if self.check(TT.RIGHT_BRACKET): break
            self.consume(TT.COMMA, "Expect ',' between list items.")

        self.consume(TT.RIGHT_BRACKET, "Expect ']' after list items.")
        return ListExpr(items)

    def statement(self) -> Stmt:
        if self.match(TT.FOR): return self.for_statement()
        if self.match(TT.IF): return self.if_statement()
        if self.match(TT.PRINT): return self.print_statement()
        if self.match(TT.RETURN): return self.return_statement()
        if self.match(TT.WHILE): return self.while_statement()
        if self.match(TT.LEFT_BRACE): return BlockStmt(self.block())

        return self.expression_statement()

    def block(self) -> list[Stmt]:
        statements = []

        while not self.check(TT.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TT.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def for_statement(self) -> Stmt:
        self.consume(TT.LEFT_PAREN, "Expect '(' after 'for'.")

        if self.match(TT.SEMICOLON):
            initializer = None
        elif self.match(TT.VAR):
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

    def if_statement(self) -> IfStmt:
        self.consume(TT.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TT.RIGHT_PAREN, "Expect ')' after 'if' condition.")

        thenBranch = self.statement()
        elseBranch = None

        if self.match(TT.ELSE):
            elseBranch = self.statement()

        return IfStmt(condition, thenBranch, elseBranch)

    def print_statement(self) -> PrintStmt:
        value = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(value)

    def return_statement(self) -> ReturnStmt:
        keyword = self.previous()
        value = None

        if not self.check(TT.SEMICOLON):
            value = self.expression()

        self.consume(TT.SEMICOLON, "Expect ';' after return value.")
        return ReturnStmt(keyword, value)

    def while_statement(self) -> WhileStmt:
        self.consume(TT.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TT.RIGHT_PAREN, "Expect ')' after 'while' condition.")

        body = self.statement()

        return WhileStmt(condition, body)

    def expression_statement(self) -> ExpressionStmt:
        expr = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStmt(expr)

    def declaration(self) -> Stmt | None:
        try:
            if self.match(TT.CLASS): return self.class_declaration()
            if self.match(TT.FUN): return self.function("function")
            if self.match(TT.VAR): return self.var_declaration()
            return self.statement()
        except Parser.ParseError:
            self.synchronize()
            return None

    def class_declaration(self):
        name = self.consume(TT.IDENTIFIER, "Expect class name.")

        superclass = None
        if self.match(TT.LESS):
            self.consume(TT.IDENTIFIER, "Expect superclass name.")
            superclass = VariableExpr(self.previous())

        self.consume(TT.LEFT_BRACE, "Expect '{' before class body.")

        methods = []
        while not self.check(TT.RIGHT_BRACE) and not self.is_at_end():
            methods.append(self.function("method"))

        self.consume(TT.RIGHT_BRACE, "Expect '}' after class body.")

        return ClassStmt(name, superclass, methods)

    def function(self, kind: str) -> FunctionStmt:
        name = self.consume(TT.IDENTIFIER, f'Expect {kind} name.')

        self.consume(TT.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []
        if not self.check(TT.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters.")
                parameters.append(self.consume(TT.IDENTIFIER, "Expect parameter name."))
                if not self.match(TT.COMMA): break
        self.consume(TT.RIGHT_PAREN, f"Expect ')' after {kind} parameters.")

        self.consume(TT.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body = self.block()

        return FunctionStmt(name, parameters, body)

    def var_declaration(self) -> VarStmt:
        name = self.consume(TT.IDENTIFIER, "Expect variable name.")

        initializer = None if not self.match(TT.EQUAL) else self.expression()

        self.consume(TT.SEMICOLON, "Expect ';' after variable declaration.")
        return VarStmt(name, initializer)

    # ----------- Helper methods ---------------
    def match(self, *t_types: TT) -> bool:
        """
        Advance if current LoxToken is one of t_types.
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

    def peek(self) -> LoxToken:
        """
        Get the current token. Do not advance/consume.
        :return: LoxToken at current
        """
        return self.tokens[self.current]

    def is_at_end(self) -> bool:
        """
        Check if parser hit end of file.
        :return: True if at EOF token, else False
        """
        return self.peek().t_type == TT.EOF

    def previous(self) -> LoxToken:
        """
        Get LoxToken at current - 1
        :return: LoxToken at current - 1
        """
        return self.tokens[self.current - 1]

    def advance(self) -> LoxToken:
        """
        Get current LoxToken and advance current pointer.
        :return: LoxToken at current
        """
        if not self.is_at_end(): self.current += 1
        return self.previous()

    def consume(self, t_type: TT, error_message: str) -> LoxToken:
        """
        Advance to next token if current token matches t_type, and return current.
        If match not found, raise error with error_message.
        :param t_type: TokenType to match at current
        :param error_message: Error message to raise if no match
        :return: current LoxToken
        :raises: ParseError if current token doesn't match t_type
        """
        if self.check(t_type): return self.advance()
        raise self.error(self.peek(), error_message)

    def error(self, token: LoxToken, message: str) -> ParseError:
        """
        Generate an error and alert Lox
        :param token: LoxToken where error occurred
        :param message: Error message
        :return: ParseError to raise
        """
        from lox.Lox import Lox
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
