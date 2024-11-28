from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from Token import Token

if TYPE_CHECKING:
	from Stmt import Expression, Print
class Visitor(ABC):
	@abstractmethod
	def visit_expression_stmt(self, expr: "Expression"): pass
	@abstractmethod
	def visit_print_stmt(self, expr: "Print"): pass

class Stmt(ABC):
	@abstractmethod
	def accept(self, visitor: "Visitor"): pass

class Expression(Stmt):
	def __init__(self, expression: "Expr", ):
		self.expression = expression
	def accept(self, visitor: "Visitor"):
		return visitor.visit_expression_stmt(self)

class Print(Stmt):
	def __init__(self, expression: "Expr", ):
		self.expression = expression
	def accept(self, visitor: "Visitor"):
		return visitor.visit_print_stmt(self)

