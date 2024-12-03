from Environment import Environment
from Expr import *
from LoxRuntimeError import LoxRuntimeError
from Stmt import *
from Token import TokenType as TT


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.environment = Environment()

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
    def visit_blockstmt(self, stmt: "BlockStmt"):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_expressionstmt(self, stmt: "ExpressionStmt"):
        return self.evaluate(stmt.expression)  # return the value here so it can be printed when in REPL

    def visit_printstmt(self, stmt: "PrintStmt"):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visit_varstmt(self, stmt: "VarStmt"):
        initializer = stmt.initializer
        value = None if initializer is None else self.evaluate(initializer)

        self.environment.define(stmt.name.lexeme, value)

    def visit_ifstmt(self, stmt: "IfStmt"):
        if self.is_truthy(self.evaluate(stmt.condition)): self.execute(stmt.thenBranch)
        elif stmt.elseBranch: self.execute(stmt.elseBranch)

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
    def visit_assignexpr(self, expr: "AssignExpr"):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_binaryexpr(self, expr: "BinaryExpr"):
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

    def visit_groupingexpr(self, expr: "GroupingExpr"):
        return self.evaluate(expr.expr)

    def visit_literalexpr(self, expr: "LiteralExpr"):
        return expr.value

    def visit_unaryexpr(self, expr: "UnaryExpr"):
        right = self.evaluate(expr.right)

        if expr.operator.t_type == TT.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)
        elif expr.operator.t_type == TT.BANG:
            return not self.is_truthy(right)

    def visit_variableexpr(self, expr: "VariableExpr"):
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
