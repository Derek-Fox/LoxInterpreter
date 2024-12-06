from Expr import *
from Stmt import *
from Interpreter import Interpreter


class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes: list[dict] = []

    # -------- Stmt Visitor methods -------
    def visit_block_stmt(self, stmt: "BlockStmt"):
        self.begin_scope()
        self.resolve_all(stmt.statements)
        self.end_scope()

    def visit_expression_stmt(self, stmt: "ExpressionStmt"):
        self.resolve(stmt.expression)

    def visit_function_stmt(self, stmt: "FunctionStmt"):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt)

    def visit_if_stmt(self, stmt: "IfStmt"):
        self.resolve(stmt.condition)
        self.resolve(stmt.thenBranch)
        if stmt.elseBranch: self.resolve(stmt.elseBranch)

    def visit_print_stmt(self, stmt: "PrintStmt"):
        self.resolve(stmt.expression)

    def visit_return_stmt(self, stmt: "ReturnStmt"):
        if stmt.value: self.resolve(stmt.value)

    def visit_var_stmt(self, stmt: "VarStmt"):
        self.declare(stmt.name)

        if stmt.initializer:
            self.resolve(stmt.initializer)

        self.define(stmt.name)

    def visit_while_stmt(self, stmt: "WhileStmt"):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)

    # ------- Expr Visitor methods ----------
    def visit_assign_expr(self, expr: "AssignExpr"):
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_binary_expr(self, expr: "BinaryExpr"):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_call_expr(self, expr: "CallExpr"):
        self.resolve(expr.callee)

        for argument in expr.arguments:
            self.resolve(argument)

    def visit_grouping_expr(self, expr: "GroupingExpr"):
        self.resolve(expr.expression)

    def visit_literal_expr(self, expr: "LiteralExpr"):
        pass

    def visit_logical_expr(self, expr: "LogicalExpr"):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_unary_expr(self, expr: "UnaryExpr"):
        self.resolve(expr.right)

    def visit_variable_expr(self, expr: "VariableExpr"):
        if self.scopes and not self.scopes[-1][expr.name.lexeme]:
            self.error(expr.name, "Can't read local variable in its own initializer.")

        self.resolve_local(expr, expr.name)

    # ------ Shared visitor methods ----------
    def resolve(self, thing: Stmt | Expr):
        thing.accept(self)

    def resolve_all(self, things: list[Stmt | Expr]):
        for thing in things:
            self.resolve(thing)

    # ------- Helper methods ---------
    def declare(self, name: "Token"):
        if not self.scopes: return

        self.scopes[-1][name.lexeme] = False

    def define(self, name: "Token"):
        if not self.scopes: return

        self.scopes[-1][name.lexeme] = True

    def resolve_local(self, expr: "Expr", name: "Token"):
        for i, scope in enumerate(reversed(scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, i)  # TODO: implement this method!
                return

    def resolve_function(self, function: FunctionStmt):
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve_all(function.body)
        self.end_scope()

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    @classmethod
    def error(cls, token: "Token", message: str):
        from Lox import Lox
        Lox.error_token(token, message)
