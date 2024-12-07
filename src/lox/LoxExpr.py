from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from lox.LoxToken import LoxToken

if TYPE_CHECKING:
	from Expr import AssignExpr, BinaryExpr, CallExpr, GetExpr, GroupingExpr, LiteralExpr, LogicalExpr, SetExpr, SuperExpr, ThisExpr, UnaryExpr, VariableExpr
class ExprVisitor(ABC):
	@abstractmethod
	def visit_assign_expr(self, expr: "AssignExpr"): pass
	@abstractmethod
	def visit_binary_expr(self, expr: "BinaryExpr"): pass
	@abstractmethod
	def visit_call_expr(self, expr: "CallExpr"): pass
	@abstractmethod
	def visit_get_expr(self, expr: "GetExpr"): pass
	@abstractmethod
	def visit_grouping_expr(self, expr: "GroupingExpr"): pass
	@abstractmethod
	def visit_literal_expr(self, expr: "LiteralExpr"): pass
	@abstractmethod
	def visit_logical_expr(self, expr: "LogicalExpr"): pass
	@abstractmethod
	def visit_set_expr(self, expr: "SetExpr"): pass
	@abstractmethod
	def visit_super_expr(self, expr: "SuperExpr"): pass
	@abstractmethod
	def visit_this_expr(self, expr: "ThisExpr"): pass
	@abstractmethod
	def visit_unary_expr(self, expr: "UnaryExpr"): pass
	@abstractmethod
	def visit_variable_expr(self, expr: "VariableExpr"): pass

class Expr(ABC):
	@abstractmethod
	def accept(self, visitor: "ExprVisitor"): pass

class AssignExpr(Expr):
	def __init__(self, name: "LoxToken", value: "Expr", ):
		self.name = name
		self.value = value
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_assign_expr(self)

class BinaryExpr(Expr):
	def __init__(self, left: "Expr", operator: "LoxToken", right: "Expr", ):
		self.left = left
		self.operator = operator
		self.right = right
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_binary_expr(self)

class CallExpr(Expr):
	def __init__(self, callee: "Expr", paren: "LoxToken", arguments: "list[Expr]", ):
		self.callee = callee
		self.paren = paren
		self.arguments = arguments
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_call_expr(self)

class GetExpr(Expr):
	def __init__(self, object: "Expr", name: "LoxToken", ):
		self.object = object
		self.name = name
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_get_expr(self)

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

class LogicalExpr(Expr):
	def __init__(self, left: "Expr", operator: "LoxToken", right: "Expr", ):
		self.left = left
		self.operator = operator
		self.right = right
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_logical_expr(self)

class SetExpr(Expr):
	def __init__(self, object: "Expr", name: "LoxToken", value: "Expr", ):
		self.object = object
		self.name = name
		self.value = value
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_set_expr(self)

class SuperExpr(Expr):
	def __init__(self, keyword: "LoxToken", method: "LoxToken", ):
		self.keyword = keyword
		self.method = method
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_super_expr(self)

class ThisExpr(Expr):
	def __init__(self, keyword: "LoxToken", ):
		self.keyword = keyword
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_this_expr(self)

class UnaryExpr(Expr):
	def __init__(self, operator: "LoxToken", right: "Expr", ):
		self.operator = operator
		self.right = right
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_unary_expr(self)

class VariableExpr(Expr):
	def __init__(self, name: "LoxToken", ):
		self.name = name
	def accept(self, visitor: "ExprVisitor"):
		return visitor.visit_variable_expr(self)

