import abc
import inspect
import math

from lox.LoxEnvironment import Environment
from lox.LoxExpr import *
from lox.LoxCallable import LoxCallable
from lox.LoxClass import LoxClass
from lox.LoxFunction import LoxFunction
from lox.LoxInstance import LoxInstance
from lox.LoxRuntimeError import LoxRuntimeError
from lox.LoxReturn import LoxReturn
from lox.LoxStmt import *
from lox.LoxToken import TokenType as TT
import lox.NativeFunctions
from lox.NativeFunctions import NativeFunction


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.locals: dict[Expr, int] = {}

        self.define_global_constants()
        self.define_native_functions()

    def define_global_constants(self):
        self.globals.define("PI", math.pi)
        self.globals.define("E", math.e)

    def define_native_functions(self):
        ignore = [LoxCallable, LoxRuntimeError, lox.NativeFunctions.NativeFunction, abc.ABC]
        for _, obj in inspect.getmembers(lox.NativeFunctions,
                                         predicate=lambda x: inspect.isclass(x) and x not in ignore):
            self.globals.define(obj.name, obj())

    def interpret(self, statements: list[Stmt], repl: bool = False):
        """
        Run the interpreter on input statements.
        :param statements: list of statements to run through interpreter
        :param repl: whether to print the output of expressions immediately after running (for repl)
        """
        try:
            for stmt in statements:
                ret = self.execute(stmt)
                if ret is not None and repl: print(self.stringify(ret))  # print the return of expressions in repl
        except LoxRuntimeError as error:
            from lox.Lox import Lox
            Lox.runtime_error(error)

    # --------- Stmt Visitor Methods ---------
    def visit_block_stmt(self, stmt: "BlockStmt"):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_class_stmt(self, stmt: "ClassStmt"):
        superclass = None
        if stmt.superclass:
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, LoxClass):
                raise LoxRuntimeError(stmt.superclass.name, "Superclass must be a class.")

        self.environment.define(stmt.name.lexeme, None)

        if stmt.superclass:
            self.environment = Environment(self.environment)
            self.environment.define("super", superclass)

        methods = {
            method.name.lexeme: LoxFunction(method, self.environment, method.name.lexeme == 'init')
            for method in stmt.methods
        }

        l_class = LoxClass(stmt.name.lexeme, superclass, methods)

        if stmt.superclass:
            self.environment = self.environment.enclosing

        self.environment.assign(stmt.name, l_class)

    def visit_expression_stmt(self, stmt: "ExpressionStmt"):
        return self.evaluate(stmt.expression)  # return the value here so it can be printed when in REPL

    def visit_function_stmt(self, stmt: "FunctionStmt"):
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)

    def visit_var_stmt(self, stmt: "VarStmt"):
        initializer = stmt.initializer
        value = None if initializer is None else self.evaluate(initializer)

        self.environment.define(stmt.name.lexeme, value)

    def visit_if_stmt(self, stmt: "IfStmt"):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch:
            self.execute(stmt.elseBranch)

    def visit_return_stmt(self, stmt: "ReturnStmt"):
        value = None
        if stmt.value:
            value = self.evaluate(stmt.value)

        raise LoxReturn(value)

    def visit_while_stmt(self, stmt: "WhileStmt"):
        while self.is_truthy(self.evaluate(stmt.condition)): self.execute(stmt.body)

    def execute(self, stmt: Stmt):
        return stmt.accept(self)

    def execute_block(self, statements: list[Stmt], environment: Environment):
        previous = self.environment

        try:
            self.environment = environment
            for stmt in statements:
                self.execute(stmt)
        finally:
            self.environment = previous

    # -------- Expr Visitor methods ---------
    def visit_access_expr(self, expr: "AccessExpr"):
        lst, index = self.validate_list_indexing(expr)
        return lst[int(index)]

    def visit_assign_expr(self, expr: "AssignExpr"):
        value = self.evaluate(expr.value)

        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)

        return value

    def visit_binary_expr(self, expr: "BinaryExpr"):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.t_type:
            case TT.MINUS | TT.MINUS_EQUAL | TT.MINUS_MINUS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TT.SLASH | TT.SLASH_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                if float(right) == 0: raise LoxRuntimeError(expr.operator, "Cannot divide by 0.")
                return float(left) / float(right)
            case TT.STAR | TT.STAR_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right)
            case TT.CARAT:
                self.check_number_operands(expr.operator, left, right)
                return float(left) ** float(right)
            case TT.PLUS | TT.PLUS_EQUAL | TT.PLUS_PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, list):
                    left = list(left)
                    left.append(right)
                    return left
                if isinstance(left, str) or isinstance(right, str):
                    return self.stringify(left) + self.stringify(right)
                raise LoxRuntimeError(expr.operator, "Unsupported types for addition.")
            case TT.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TT.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TT.LESS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TT.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            case TT.EQUAL_EQUAL:
                return left == right
            case TT.BANG_EQUAL:
                return left != right

    def visit_call_expr(self, expr: "CallExpr"):
        callee = self.evaluate(expr.callee)

        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")

        num_args = len(arguments)
        arity = callee.arity()

        if num_args != arity:
            raise LoxRuntimeError(expr.paren, f"Expected {arity} arguments but got {num_args}.")

        try:
            retval = callee.call(self, arguments)
            return retval
        except LoxRuntimeError as call_error:
            raise LoxRuntimeError(expr.paren, call_error.message)

    def visit_get_expr(self, expr: "GetExpr"):
        obj = self.evaluate(expr.object)

        if isinstance(obj, LoxInstance):
            return obj.get(expr.name)

        raise LoxRuntimeError(expr.name, "Only instances have properties.")

    def visit_grouping_expr(self, expr: "GroupingExpr"):
        return self.evaluate(expr.expression)

    def visit_list_expr(self, expr: "ListExpr"):
        return [self.evaluate(item) for item in expr.items]

    def visit_listassign_expr(self, expr: "ListAssignExpr"):
        lst, idx = self.validate_list_indexing(expr)
        lst[idx] = self.evaluate(expr.value)
        return lst

    def visit_literal_expr(self, expr: "LiteralExpr"):
        return expr.value

    def visit_logical_expr(self, expr: "LogicalExpr"):
        left = self.evaluate(expr.left)

        # attempt to short circuit
        if expr.operator.t_type == TT.OR:
            if self.is_truthy(left): return left  # for OR, if first is true, return it
        else:
            if not self.is_truthy(left): return left  # for AND, if first is false, return it

        return self.evaluate(expr.right)  # have to evaluate the second operand_

    def visit_set_expr(self, expr: "SetExpr"):
        obj = self.evaluate(expr.object)

        if not isinstance(obj, LoxInstance):
            raise LoxRuntimeError(expr.name, "Only instances have fields.")

        value = self.evaluate(expr.value)
        obj.set(expr.name, value)
        return value

    def visit_super_expr(self, expr: "SuperExpr"):
        distance = self.locals.get(expr)
        superclass: LoxClass = self.environment.get_at(distance, "super")

        obj: LoxInstance = self.environment.get_at(distance - 1, "this")  # get current instance

        method = superclass.find_method(expr.method.lexeme)

        if not method:
            raise LoxRuntimeError(expr.method, f"Undefined property '{expr.method.lexeme}'.")
        return method.bind(obj)

    def visit_this_expr(self, expr: "ThisExpr"):
        return self.look_up_variable(expr.keyword, expr)

    def visit_unary_expr(self, expr: "UnaryExpr"):
        right = self.evaluate(expr.right)

        match expr.operator.t_type:
            case TT.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)
            case TT.BANG:
                return not self.is_truthy(right)

    def visit_variable_expr(self, expr: "VariableExpr"):
        return self.look_up_variable(expr.name, expr)

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    # ------------- Helper methods ----------
    @classmethod
    def is_truthy(cls, obj: object) -> bool:
        """
        Check if obj is truthy. Only nil and false are falsey.
        :param obj: object to test
        :return: True or False
        """
        if obj is None: return False
        if isinstance(obj, bool): return bool(obj)
        return True

    @classmethod
    def check_number_operand(cls, operator: LoxToken, operand: object):
        """
        Check that operand is a number. Lox only uses floats internally.
        :param operator: Operator which is expecting a number.
        :param operand: Operand which should be a number.
        :raises: LoxRuntimeError if check fails.
        """
        if isinstance(operand, float): return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    @classmethod
    def check_number_operands(cls, operator: LoxToken, left: object, right: object):
        """
        Check that operands are numbers. Lox only uses floats internally.
        :param operator: Operator which is expecting 2 numbers.
        :param left: Operand which should be a number.
        :param right: Operand which should be a number.
        :raises: LoxRuntimeError if check fails.
        """
        if isinstance(left, float) and isinstance(right, float): return
        raise LoxRuntimeError(operator, "Both Operands must be numbers.")

    @classmethod
    def stringify(cls, obj: object) -> str:
        """
        Return string representation of object.
        :param obj: Object to stringify.
        :return: String representation of obj
        """
        if obj is None: return 'nil'
        if isinstance(obj, float):
            text = str(obj)
            return text if text[-2:] != ".0" else text[:-2]
        if isinstance(obj, bool):
            return str(obj).lower()  # why does python have capitalized bools??
        if isinstance(obj, list):
            item_strs = [cls.stringify(item) for item in obj]
            return f"[{', '.join(item_strs)}]"
        return str(obj)

    def validate_list_indexing(self, expr: AccessExpr | ListAssignExpr) -> tuple[list, int]:
        lst = self.evaluate(expr.lst)
        if not isinstance(lst, list):
            raise LoxRuntimeError(expr.name, "Can only access index of lists.")

        index = self.evaluate(expr.index)
        if not (isinstance(index, float) and float(index).is_integer()):
            raise LoxRuntimeError(expr.name, "Can only index with a whole number.")

        length = len(lst)
        if index >= length or index < -length:
            raise LoxRuntimeError(expr.name, "List index out of range.")

        return lst, int(index)

    def resolve(self, expr: Expr, depth: int):
        """
        Mark the resolution depth for a given expr, for use when looking up variable exprs.
        :param expr: Expression to resolve depth of
        :param depth: how many environments deep is the expr
        """
        self.locals[expr] = depth

    def look_up_variable(self, name: LoxToken, expr: Expr) -> object:
        """
        Look up variable in environment hierarchy.
        :param name: Variable name Token to look for
        :param expr: Expr to fetch distance from self.locals for (to tell how deep to search environment hierarchy)
        """
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        else:
            return self.globals.get(name)
