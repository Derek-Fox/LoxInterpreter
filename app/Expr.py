from abc import ABC, abstractmethod
from Token import Token

class Expr(ABC): pass

class Binary(Expr):
	def __init__(self, left: Expr, op: Token, right: Expr, ):
		self.left = left
		self.op = op
		self.right = right


class Grouping(Expr):
	def __init__(self, expr: Expr, ):
		self.expr = expr


class Literal(Expr):
	def __init__(self, value: object, ):
		self.value = value


class Unary(Expr):
	def __init__(self, op: Token, right: Expr, ):
		self.op = op
		self.right = right


