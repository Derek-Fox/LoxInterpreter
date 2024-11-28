from Expr import *
from Token import TokenType as TT
from LoxRuntimeError import LoxRuntimeError


class Interpreter(Visitor):
    def interpret(self, expression: Expr):
        """
        Run the interpreter on input expression.
        :param expression: Expression to run through interpreter.
        """
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except LoxRuntimeError as error:
            from Lox import Lox
            Lox.runtime_error(error)

    # -------- Visitor methods ---------

    def visit_binary_expr(self, expr: "Binary"):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.t_type:
            case TT.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TT.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case TT.STAR:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right)
            case TT.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) or isinstance(right, str):
                    return self.stringify(left) + self.stringify(right)
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

    def visit_grouping_expr(self, expr: "Grouping"):
        return self.evaluate(expr.expr)

    def visit_literal_expr(self, expr: "Literal"):
        return expr.value

    def visit_unary_expr(self, expr: "Unary"):
        right = self.evaluate(expr.right)

        if expr.operator.t_type == TT.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)
        elif expr.operator.t_type == TT.BANG:
            return not self.is_truthy(right)

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
    def check_number_operands(cls, operator: Token, left, right):
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
