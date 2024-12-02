from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from Token import Token

if TYPE_CHECKING:
	from Expr import CallExpr, LogicalExpr, AssignExpr, BinaryExpr, GroupingExpr, LiteralExpr, UnaryExpr, VariableExpr
class ExprVisitor(ABC):
	@abstractmethod
	def visit_call_expr(self, expr: "CallExpr"): pass
	@abstractmethod
	def visit_logical_expr(self, expr: "LogicalExpr"): pass
	@abstractmethod
	def visit_assign_expr(self, expr: "AssignExpr"): pass
	@abstractmethod
	def visit_binary_expr(self, expr: "BinaryExpr"): pass
	@abstractmethod
	def visit_grouping_expr(self, expr: "GroupingExpr"): pass
	@abstractmethod
	def visit_literal_expr(self, expr: "LiteralExpr"): pass
	@abstractmethod
	def visit_unary_expr(self, expr: "UnaryExpr"): pass
	@abstractmethod
	def visit_variable_expr(self, expr: "VariableExpr"): pass

class Expr(ABC):
	@abstractmethod
	def accept(self, visitor: "ExprVisitor"): pass

class CallExpr(Expr):
	def __init__(self, callee: "Expr", paren: "Token", arguments: "list[Expr]", ):
		self.callee = callee
		self.paren = paren
		self.arguments = arguments
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_call_expr(self)

class LogicalExpr(Expr):
	def __init__(self, left: "Expr", operator: "Token", right: "Expr", ):
		self.left = left
		self.operator = operator
		self.right = right
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_logical_expr(self)

class AssignExpr(Expr):
	def __init__(self, name: "Token", value: "Expr", ):
		self.name = name
		self.value = value
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_assign_expr(self)

class BinaryExpr(Expr):
	def __init__(self, left: "Expr", operator: "Token", right: "Expr", ):
		self.left = left
		self.operator = operator
		self.right = right
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_binary_expr(self)

class GroupingExpr(Expr):
	def __init__(self, expression: "Expr", ):
		self.expression = expression
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_grouping_expr(self)

class LiteralExpr(Expr):
	def __init__(self, value: "object", ):
		self.value = value
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_literal_expr(self)

class UnaryExpr(Expr):
	def __init__(self, operator: "Token", right: "Expr", ):
		self.operator = operator
		self.right = right
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_unary_expr(self)

class VariableExpr(Expr):
	def __init__(self, name: "Token", ):
		self.name = name
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_variable_expr(self)

