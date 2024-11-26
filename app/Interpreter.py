from Expr import *
from Token import TokenType as TT


class Interpreter(Visitor):
    def visit_binary_expr(self, expr: "Binary"):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.op.t_type:
            case TT.MINUS:
                return float(left) - float(right)
            case TT.SLASH:
                return float(left) / float(right)
            case TT.STAR:
                return float(left) * float(right)
            case TT.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)

    def visit_grouping_expr(self, expr: "Grouping"):
        return self.evaluate(expr.expr)

    def visit_literal_expr(self, expr: "Literal"):
        return expr.value

    def visit_unary_expr(self, expr: "Unary"):
        right = self.evaluate(expr.right)

        if expr.op.t_type == TT.MINUS:
            return -float(right)
        elif expr.op.t_type == TT.BANG:
            return not is_truthy(right)

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    @classmethod
    def is_truthy(cls, obj: object) -> bool:
        if obj is None: return False
        if isinstance(obj, bool): return bool(obj)
        return True
