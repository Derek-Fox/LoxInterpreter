from Expr import *


class AstPrinter(Visitor):
    def print(self, expr: Expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr: Binary):
        return self.parenthesize(expr.op.lexeme, [expr.left, expr.right])

    def visitGroupingExpr(self, expr: Grouping):
        return self.parenthesize('grouping', [expr.expr])

    def visitLiteralExpr(self, expr: Literal):
        return 'nil' if not expr.value else str(expr.value)

    def visitUnaryExpr(self, expr: Unary):
        return self.parenthesize(expr.op.lexeme, [expr.right])

    def parenthesize(self, name: str, exprs: list[Expr]) -> str:
        res = [f'({name}']

        for expr in exprs:
            res.append(f' {expr.accept(self)}')
        res.append(')')

        return ''.join(res)