from Expr import *


class RpnPrinter(Visitor):
    def print(self, expr: Expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr: "Binary"):
        return self.RpnFormat(expr.op.lexeme, [expr.left, expr.right])

    def visitGroupingExpr(self, expr: "Grouping"):
        return self.RpnFormat('grouping', [expr.expr])

    def visitLiteralExpr(self, expr: "Literal"):
        return 'nil' if not expr.value else str(expr.value)

    def visitUnaryExpr(self, expr: "Unary"):
        return self.RpnFormat(expr.op.lexeme, [expr.right])

    def RpnFormat(self, name: str, exprs: list[Expr]):
        res = []

        for expr in exprs:
            res.append(f'{expr.accept(self)} ')
        res.append(f'{name}')

        return ''.join(res)
