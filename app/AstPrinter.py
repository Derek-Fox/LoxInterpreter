from Expr import *


class AstPrinter(ExprVisitor):
    def print(self, expr: Expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, [expr.left, expr.right])

    def visit_grouping_expr(self, expr: Grouping):
        return self.parenthesize('grouping', [expr.expr])

    def visit_literal_expr(self, expr: Literal):
        return 'nil' if not expr.value else str(expr.value)

    def visit_unary_expr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, [expr.right])

    def parenthesize(self, name: str, exprs: list[Expr]) -> str:
        res = [f'({name}']

        for expr in exprs:
            res.append(f' {expr.accept(self)}')
        res.append(')')

        return ''.join(res)