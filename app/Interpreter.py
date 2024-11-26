from Expr import *


class Interpreter(Visitor):
    def visit_binary_expr(self, expr: "Binary"):
        pass

    def visit_grouping_expr(self, expr: "Grouping"):
        return evaluate(expr.expr)

    def visit_literal_expr(self, expr: "Literal"):
        return expr.value

    def visit_unary_expr(self, expr: "Unary"):
        pass

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)
