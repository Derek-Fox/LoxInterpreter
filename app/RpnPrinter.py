from Expr import *


class RpnPrinter(Visitor):
    def print(self, expr: Expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr: "Binary"):
        return self.format(expr.operator.lexeme, [expr.left, expr.right])

    def visit_grouping_expr(self, expr: "Grouping"):
        return self.format('grouping', [expr.expr])

    def visit_literal_expr(self, expr: "Literal"):
        return 'nil' if not expr.value else str(expr.value)

    def visit_unary_expr(self, expr: "Unary"):
        return self.format(expr.operator.lexeme, [expr.right])

    def format(self, name: str, exprs: list[Expr]):
        res = []

        for expr in exprs:
            res.append(f'{expr.accept(self)} ')
        res.append(f'{name}')

        return ''.join(res)
