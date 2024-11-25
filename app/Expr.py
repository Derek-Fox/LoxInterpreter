from abc import ABC, abstractmethod
from Token import Token

class Expr(ABC):
	@abstractmethod
	def accept(self, visitor: Visitor): pass
class Visitor(ABC):
	@abstractmethod
	def visitBinaryExpr(self, expr: Binary): pass
	@abstractmethod
	def visitGroupingExpr(self, expr: Grouping): pass
	@abstractmethod
	def visitLiteralExpr(self, expr: Literal): pass
	@abstractmethod
	def visitUnaryExpr(self, expr: Unary): pass

class Binary(Expr):
	def __init__(self, left: Expr, op: Token, right: Expr, ):
		self.left = left
		self.op = op
		self.right = right
	def accept(self, visitor: Visitor):
		visitor.visit(self)

class Grouping(Expr):
	def __init__(self, expr: Expr, ):
		self.expr = expr
	def accept(self, visitor: Visitor):
		visitor.visit(self)

class Literal(Expr):
	def __init__(self, value: object, ):
		self.value = value
	def accept(self, visitor: Visitor):
		visitor.visit(self)

class Unary(Expr):
	def __init__(self, op: Token, right: Expr, ):
		self.op = op
		self.right = right
	def accept(self, visitor: Visitor):
		visitor.visit(self)

