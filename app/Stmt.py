from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from Token import Token

if TYPE_CHECKING:
	from Stmt import Expression, Print, Var
class StmtVisitor(ABC):
	@abstractmethod
	def visit_expression_stmt(self, expr: "Expression"): pass
	@abstractmethod
	def visit_print_stmt(self, expr: "Print"): pass
	@abstractmethod
	def visit_var_stmt(self, expr: "Var"): pass

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

class Var(Stmt):
	def __init__(self, name: "Token", initializer: "Expr", ):
		self.name = name
		self.initializer = initializer
	def accept(self, visitor: "Visitor"):
		return visitor.visit_var_stmt(self)

