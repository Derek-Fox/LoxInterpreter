from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from Token import Token

if TYPE_CHECKING:
	from Expr import LogicalExpr, AssignExpr, BinaryExpr, GroupingExpr, LiteralExpr, UnaryExpr, VariableExpr
class ExprVisitor(ABC):
	@abstractmethod
	def visit_logicalexpr(self, expr: "LogicalExpr"): pass
	@abstractmethod
	def visit_assignexpr(self, expr: "AssignExpr"): pass
	@abstractmethod
	def visit_binaryexpr(self, expr: "BinaryExpr"): pass
	@abstractmethod
	def visit_groupingexpr(self, expr: "GroupingExpr"): pass
	@abstractmethod
	def visit_literalexpr(self, expr: "LiteralExpr"): pass
	@abstractmethod
	def visit_unaryexpr(self, expr: "UnaryExpr"): pass
	@abstractmethod
	def visit_variableexpr(self, expr: "VariableExpr"): pass

class Expr(ABC):
	@abstractmethod
	def accept(self, visitor: "ExprVisitor"): pass

class LogicalExpr(Expr):
	def __init__(self, left: "Expr", operator: "Token", right: "Expr", ):
		self.left = left
		self.operator = operator
		self.right = right
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_logicalexpr(self)

class AssignExpr(Expr):
	def __init__(self, name: "Token", value: "Expr", ):
		self.name = name
		self.value = value
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_assignexpr(self)

class BinaryExpr(Expr):
	def __init__(self, left: "Expr", operator: "Token", right: "Expr", ):
		self.left = left
		self.operator = operator
		self.right = right
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_binaryexpr(self)

class GroupingExpr(Expr):
	def __init__(self, expression: "Expr", ):
		self.expression = expression
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_groupingexpr(self)

class LiteralExpr(Expr):
	def __init__(self, value: "object", ):
		self.value = value
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_literalexpr(self)

class UnaryExpr(Expr):
	def __init__(self, operator: "Token", right: "Expr", ):
		self.operator = operator
		self.right = right
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_unaryexpr(self)

class VariableExpr(Expr):
	def __init__(self, name: "Token", ):
		self.name = name
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_variableexpr(self)

