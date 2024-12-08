import sys


def define_subclass(file, superclass: str, subclass: str, fields: dict[str, str]):
    file.write(f'class {subclass}{superclass}({superclass}):\n')

    file.write(f'\tdef __init__(self, ')
    for name, type in fields.items():
        file.write(f'{name}: "{type}", ')
    file.write('):\n')

    for name in fields.keys():
        file.write(f'\t\tself.{name} = {name}\n')

    file.write(f'\tdef accept(self, visitor: "{superclass}Visitor"):\n')
    file.write(f'\t\treturn visitor.visit_{subclass.lower()}_{superclass.lower()}(self)\n')
    file.write('\n')


def define_superclass(file, superclass):
    file.write(f'class {superclass}(ABC):\n')
    file.write('\t@abstractmethod\n')
    file.write(f'\tdef accept(self, visitor: "{superclass}Visitor"): pass\n\n')


def define_visitor(file, superclass: str, subclasses: dict):
    file.write(f'class {superclass}Visitor(ABC):\n')
    for subclass in subclasses.keys():
        file.write('\t@abstractmethod\n')
        file.write(f'\tdef visit_{subclass.lower()}_{superclass.lower()}')
        file.write(f'(self, {superclass.lower()}: "{subclass}{superclass}"): pass\n')
    file.write('\n')


def write_imports(file):
    file.write('from abc import ABC, abstractmethod\n')
    file.write('from typing import TYPE_CHECKING\n')
    file.write('from lox.LoxToken import LoxToken\n')
    file.write('\n')


def define_ast(output_dir: str, superclass: str, subclasses: dict[str, dict[str, str]]):
    path = f'{output_dir}/Lox{superclass}.py'
    with open(path, 'w') as file:
        write_imports(file)

        define_visitor(file, superclass, subclasses)

        define_superclass(file, superclass)

        for class_name, fields in subclasses.items():
            define_subclass(file, superclass, class_name, fields)


def define_stmt_classes(output_dir):
    superclass = 'Stmt'
    subclasses = {
        'Block': {'statements': 'list[Stmt]'},
        'Class': {'name': 'LoxToken', 'superclass': 'VariableExpr', 'methods': 'list[FunctionStmt]'},
        'Expression': {'expression': 'Expr'},
        'Function': {'name': 'LoxToken', 'params': 'list[LoxToken]', 'body': 'list[Stmt]'},
        'If': {'condition': 'Expr', 'thenBranch': 'Stmt', 'elseBranch': 'Stmt'},
        'Print': {'expression': 'Expr'},
        'Return': {'keyword': 'LoxToken', 'value': 'Expr'},
        'Var': {'name': 'LoxToken', 'initializer': 'Expr'},
        'While': {'condition': 'Expr', 'body': 'Stmt'}
    }
    define_ast(output_dir, superclass, subclasses)


def define_expr_classes(output_dir):
    superclass = "Expr"
    types = {
        'Assign': {'name': 'LoxToken', 'value': 'Expr'},
        'Binary': {'left': 'Expr', 'operator': 'LoxToken', 'right': 'Expr'},
        'Call': {'callee': 'Expr', 'paren': 'LoxToken', 'arguments': 'list[Expr]'},
        'Get': {'object': 'Expr', 'name': 'LoxToken'},
        'Grouping': {'expression': 'Expr'},
        'List': {'items': 'list[Expr]'},
        'Literal': {'value': 'object'},
        'Logical': {'left': 'Expr', 'operator': 'LoxToken', 'right': 'Expr'},
        'Set': {'object': 'Expr', 'name': 'LoxToken', 'value': 'Expr'},
        'Super': {'keyword': 'LoxToken', 'method': 'LoxToken'},
        'This': {'keyword': 'LoxToken'},
        'Unary': {'operator': 'LoxToken', 'right': 'Expr'},
        'Variable': {'name': 'LoxToken'}
    }
    define_ast(output_dir, superclass, types)


def main():
    if len(sys.argv) != 2:
        print('Usage: python GenerateAst.py <output dir>')
        return

    output_dir = sys.argv[1]

    define_expr_classes(output_dir)

    define_stmt_classes(output_dir)


if __name__ == '__main__':
    main()
