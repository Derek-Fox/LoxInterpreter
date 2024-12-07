from enum import Enum, auto

from Expr import *
from Interpreter import Interpreter
from Stmt import *


class FunctionType(Enum):
    NONE = auto(),
    FUNCTION = auto(),
    INITIALIZER = auto(),
    METHOD = auto()


class ClassType(Enum):
    NONE = auto()
    CLASS = auto()


class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes: list[dict[str, bool]] = []
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE

    # -------- Stmt Visitor methods -------
    def visit_block_stmt(self, stmt: "BlockStmt"):
        self.begin_scope()
        self.resolve_all(stmt.statements)
        self.end_scope()

    def visit_class_stmt(self, stmt: "ClassStmt"):
        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS

        self.declare(stmt.name)
        self.define(stmt.name)

        if stmt.superclass:
            if stmt.name.lexeme == stmt.superclass.name.lexeme:
                self.error(stmt.superclass.name, "A class can't inherit from itself.")

            self.resolve(stmt.superclass)

            self.begin_scope()  # scope to look up 'super' keyword
            self.peek_scope()["super"] = True

        self.begin_scope()  # scope to look up 'this' keyword
        self.peek_scope()['this'] = True

        for method in stmt.methods:
            declaration = FunctionType.INITIALIZER if method.name.lexeme == "init" else FunctionType.METHOD
            self.resolve_function(method, declaration)

        self.end_scope()  # end 'this' scope

        if stmt.superclass: self.end_scope()  # end 'super' scope

        self.current_class = enclosing_class

    def visit_expression_stmt(self, stmt: "ExpressionStmt"):
        self.resolve(stmt.expression)

    def visit_function_stmt(self, stmt: "FunctionStmt"):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.FUNCTION)

    def visit_if_stmt(self, stmt: "IfStmt"):
        self.resolve(stmt.condition)
        self.resolve(stmt.thenBranch)
        if stmt.elseBranch: self.resolve(stmt.elseBranch)

    def visit_print_stmt(self, stmt: "PrintStmt"):
        self.resolve(stmt.expression)

    def visit_return_stmt(self, stmt: "ReturnStmt"):
        if self.current_function == FunctionType.NONE:
            self.error(stmt.keyword, "Can't return when not in a function.")

        if stmt.value:
            if self.current_function == FunctionType.INITIALIZER:
                self.error(stmt.keyword, "Can't return a value from an initializer.")

            self.resolve(stmt.value)

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

    def visit_get_expr(self, expr: "GetExpr"):
        self.resolve(expr.object)

    def visit_grouping_expr(self, expr: "GroupingExpr"):
        self.resolve(expr.expression)

    def visit_literal_expr(self, expr: "LiteralExpr"):
        pass

    def visit_logical_expr(self, expr: "LogicalExpr"):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_set_expr(self, expr: "SetExpr"):
        self.resolve(expr.value)
        self.resolve(expr.object)

    def visit_super_expr(self, expr: "SuperExpr"):
        self.resolve_local(expr, expr.keyword)

    def visit_this_expr(self, expr: "ThisExpr"):
        if self.current_class == ClassType.NONE:
            self.error(expr.keyword, "Can't use 'this' outside of a class.")
            return

        self.resolve_local(expr, expr.keyword)

    def visit_unary_expr(self, expr: "UnaryExpr"):
        self.resolve(expr.right)

    def visit_variable_expr(self, expr: "VariableExpr"):
        if self.scopes and self.peek_scope().get(expr.name.lexeme) is False:
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
        """
        Declare a variable in the scope, i.e. put it in scope dict and mark with False (uninitialized).
        :param name: Variable name Token
        """
        if not self.scopes: return

        scope = self.peek_scope()
        if name.lexeme in scope:
            self.error(name, "Already a variable with this name in this scope.")

        scope[name.lexeme] = False

    def define(self, name: "Token"):
        """
        Define a variable in the scope, i.e. mark with True in scope dict
        :param name: Variable name Token
        """
        if not self.scopes: return

        self.peek_scope()[name.lexeme] = True

    def resolve_local(self, expr: "Expr", name: "Token"):
        """
        Find the innermost environment where local variable exists and mark its depth in the interpreter.
        :param expr: Expression to mark depth of
        :param name: Variable name Token
        """
        for i, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, i)
                return

    def resolve_function(self, function: FunctionStmt, f_type: FunctionType):
        """
        Resolve a function declaration. This differs from variables because functions can call themselves.
        :param function: FunctionStmt to resolve.
        :param f_type: type of function (function, method, etc)
        """
        enclosing_function = self.current_function
        self.current_function = f_type

        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve_all(function.body)
        self.end_scope()

        self.current_function = enclosing_function

    def begin_scope(self):
        """
        Push a scope to the stack.
        """
        self.scopes.append({})

    def end_scope(self):
        """
        Pop a scope from the stack.
        """
        self.scopes.pop()

    def peek_scope(self) -> dict[str, bool]:
        """
        Peek at top of scope stack.
        :return: topmost scope (which is a dict of str -> bool)
        """
        return self.scopes[-1]

    @classmethod
    def error(cls, token: "Token", message: str):
        """
        Send an error to be reported by Lox.
        :param token: Token where error occurred.
        :param message: Error message.
        """
        from Lox import Lox
        Lox.error_token(token, message)
