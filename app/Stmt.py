from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from Token import Token

if TYPE_CHECKING:
	from Stmt import ExpressionStmt, PrintStmt, VarStmt
class StmtVisitor(ABC):
	@abstractmethod
	def visit_expressionstmt(self, expr: "ExpressionStmt"): pass
	@abstractmethod
	def visit_printstmt(self, expr: "PrintStmt"): pass
	@abstractmethod
	def visit_varstmt(self, expr: "VarStmt"): pass

class Stmt(ABC):
	@abstractmethod
	def accept(self, visitor: "StmtVisitor"): pass

class ExpressionStmt(Stmt):
	def __init__(self, expression: "Expr", ):
		self.expression = expression
	def accept(self, visitor: "Visitor"):
		return visitor.visit_expressionstmt(self)

class PrintStmt(Stmt):
	def __init__(self, expression: "Expr", ):
		self.expression = expression
	def accept(self, visitor: "Visitor"):
		return visitor.visit_printstmt(self)

class VarStmt(Stmt):
	def __init__(self, name: "Token", initializer: "Expr", ):
		self.name = name
		self.initializer = initializer
	def accept(self, visitor: "Visitor"):
		return visitor.visit_varstmt(self)

