from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from Token import Token

if TYPE_CHECKING:
    from Expr import Binary, Grouping, Literal, Unary


class Visitor(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr: "Binary"): pass

    @abstractmethod
    def visit_grouping_expr(self, expr: "Grouping"): pass

    @abstractmethod
    def visit_literal_expr(self, expr: "Literal"): pass

    @abstractmethod
    def visit_unary_expr(self, expr: "Unary"): pass


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: "Visitor"): pass


class Binary(Expr):
    def __init__(self, left: "Expr", op: "Token", right: "Expr", ):
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor: "Visitor"):
        return visitor.visit_binary_expr(self)


class Grouping(Expr):
    def __init__(self, expr: "Expr", ):
        self.expr = expr

    def accept(self, visitor: "Visitor"):
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    def __init__(self, value: "object", ):
        self.value = value

    def accept(self, visitor: "Visitor"):
        return visitor.visit_literal_expr(self)


class Unary(Expr):
    def __init__(self, op: "Token", right: "Expr", ):
        self.op = op
        self.right = right

    def accept(self, visitor: "Visitor"):
        return visitor.visit_unary_expr(self)
