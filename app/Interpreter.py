from Environment import Environment
from Expr import *
from LoxRuntimeError import LoxRuntimeError
from Stmt import *
from Token import TokenType as TT


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals

        from Clock import Clock
        self.globals.define("clock", Clock())

    def interpret(self, statements: list[Stmt], repl: bool = False):
        """
        Run the interpreter on input statements.
        :param statements: list of statements to run through interpreter
        :param repl: whether to print the output of expressions immediately after running (for repl)
        """
        try:
            for stmt in statements:
                ret = self.execute(stmt)
                if ret and repl: print(self.stringify(ret))  # print the return of expressions in repl
        except LoxRuntimeError as error:
            from Lox import Lox
            Lox.runtime_error(error)

    # --------- Stmt Visitor Methods ---------
    def visit_block_stmt(self, stmt: "BlockStmt"):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_expression_stmt(self, stmt: "ExpressionStmt"):
        return self.evaluate(stmt.expression)  # return the value here so it can be printed when in REPL

    def visit_print_stmt(self, stmt: "PrintStmt"):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visit_var_stmt(self, stmt: "VarStmt"):
        initializer = stmt.initializer
        value = None if initializer is None else self.evaluate(initializer)

        self.environment.define(stmt.name.lexeme, value)

    def visit_if_stmt(self, stmt: "IfStmt"):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch:
            self.execute(stmt.elseBranch)

    def visit_while_stmt(self, stmt: "WhileStmt"):
        while self.is_truthy(self.evaluate(stmt.condition)): self.execute(stmt.body)

    def execute(self, stmt: Stmt):
        return stmt.accept(self)

    def execute_block(self, statements: list[Stmt], environment: Environment):
        previous = self.environment

        try:
            self.environment = environment
            for stmt in statements:
                self.execute(stmt)
        finally:
            self.environment = previous

    # -------- Expr Visitor methods ---------
    def visit_call_expr(self, expr: "CallExpr"):
        callee = self.evaluate(expr.callee)

        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        from LoxCallable import LoxCallable
        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")

        num_args = len(arguments)
        arity = callee.arity()

        if num_args != arity:
            raise LoxRuntimeError(expr.paren, f"Expected {arity} arguments but got {num_args}.")

        return callee.call(self, arguments)

    def visit_logical_expr(self, expr: "LogicalExpr"):
        left = self.evaluate(expr.left)

        # attempt to short circuit
        if expr.operator.t_type == TT.OR:
            if self.is_truthy(left): return left  # for OR, if first is true, return it
        else:
            if not self.is_truthy(left): return left  # for AND, if first is false, return it

        return self.evaluate(expr.right)  # have to evaluate the second operand_

    def visit_assign_expr(self, expr: "AssignExpr"):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_binary_expr(self, expr: "BinaryExpr"):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.t_type:
            case TT.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TT.SLASH:
                self.check_number_operands(expr.operator, left, right)
                if float(right) == 0: raise LoxRuntimeError(expr.operator, "Cannot divide by 0.")
                return float(left) / float(right)
            case TT.STAR:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right)
            case TT.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) or isinstance(right, str):
                    return self.stringify(left) + self.stringify(right)
                raise LoxRuntimeError(expr.operator, "Unsupported types for addition.")
            case TT.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TT.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TT.LESS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TT.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            case TT.EQUAL_EQUAL:
                return left == right
            case TT.BANG_EQUAL:
                return left != right

    def visit_grouping_expr(self, expr: "GroupingExpr"):
        return self.evaluate(expr.expr)

    def visit_literal_expr(self, expr: "LiteralExpr"):
        return expr.value

    def visit_unary_expr(self, expr: "UnaryExpr"):
        right = self.evaluate(expr.right)

        if expr.operator.t_type == TT.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)
        elif expr.operator.t_type == TT.BANG:
            return not self.is_truthy(right)

    def visit_variable_expr(self, expr: "VariableExpr"):
        return self.environment.get(expr.name)

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    # ------------- Helper methods ----------
    @classmethod
    def is_truthy(cls, obj: object) -> bool:
        """
        Check if obj is truthy. Only None and False are falsey.
        :param obj: object to test
        :return: True or False
        """
        if obj is None: return False
        if isinstance(obj, bool): return bool(obj)
        return True

    @classmethod
    def check_number_operand(cls, operator: Token, operand: object):
        """
        Check that operand is a number. Lox only uses floats internally.
        :param operator: Operator which is expecting a number.
        :param operand: Operand which should be a number.
        :raises: LoxRuntimeError if check fails.
        """
        if isinstance(operand, float): return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    @classmethod
    def check_number_operands(cls, operator: Token, left: object, right: object):
        """
        Check that operands are numbers. Lox only uses floats internally.
        :param operator: Operator which is expecting 2 numbers.
        :param left: Operand which should be a number.
        :param right: Operand which should be a number.
        :raises: LoxRuntimeError if check fails.
        """
        if isinstance(left, float) and isinstance(right, float): return
        raise LoxRuntimeError(operator, "Both Operands must be numbers.")

    @classmethod
    def stringify(cls, obj: object) -> str:
        """
        Return string representation of object.
        :param obj: Object to stringify.
        :return: String representation of obj
        """
        if obj is None: return 'nil'
        if isinstance(obj, float):
            text = str(obj)
            return text if text[-2:] != ".0" else text[:-2]
        if isinstance(obj, bool):
            return str(obj).lower()  # why does python have capitalized bools??
        return str(obj)
