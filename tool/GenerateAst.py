import sys


def define_type(file, base_name: str, class_name: str, fields: dict[str, str]):
    file.write(f'class {class_name}{base_name}({base_name}):\n')

    file.write(f'\tdef __init__(self, ')
    for field_name, field_type in fields.items():
        file.write(f'{field_name}: "{field_type}", ')
    file.write('):\n')

    for field_name in fields.keys():
        file.write(f'\t\tself.{field_name} = {field_name}\n')

    file.write(f'\tdef accept(self, visitor: "{base_name}Visitor"):\n')
    file.write(f'\t\treturn visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n')
    file.write('\n')


def define_base(file, base_name):
    file.write(f'class {base_name}(ABC):\n')
    file.write('\t@abstractmethod\n')
    file.write(f'\tdef accept(self, visitor: "{base_name}Visitor"): pass\n\n')


def define_visitor(file, base_name: str, class_names: list[str]):
    file.write(f'class {base_name}Visitor(ABC):\n')
    for class_name in class_names:
        file.write('\t@abstractmethod\n')
        file.write(f'\tdef visit_{class_name.lower()}_{base_name.lower()}')
        file.write(f'(self, {base_name.lower()}: "{class_name}{base_name}"): pass\n')
    file.write('\n')


def write_imports(file, base_name: str, class_names: list[str]):
    file.write('from abc import ABC, abstractmethod\n')
    file.write('from typing import TYPE_CHECKING\n')
    file.write('from Token import Token\n')
    file.write('\n')
    file.write('if TYPE_CHECKING:\n')
    file.write(f'\tfrom {base_name} import ')
    file.write(', '.join([f'{class_name}{base_name}' for class_name in class_names]))
    file.write('\n')


def define_ast(output_dir: str, base_name: str, types: dict[str, dict[str, str]]):
    path = f'{output_dir}/{base_name}.py'
    class_names = list(types.keys())

    with open(path, 'w') as file:
        write_imports(file, base_name, class_names)

        define_visitor(file, base_name, class_names)

        define_base(file, base_name)

        for class_name, fields in types.items():
            define_type(file, base_name, class_name, fields)


def define_stmt_classes(output_dir):
    base_class = 'Stmt'
    types = {
        'Block': {'statements': 'list[Stmt]'},
        'Class': {'name': 'Token', 'superclass': 'VariableExpr', 'methods': 'list[FunctionStmt]'},
        'Expression': {'expression': 'Expr'},
        'Function': {'name': 'Token', 'params': 'list[Token]', 'body': 'list[Stmt]'},
        'If': {'condition': 'Expr', 'thenBranch': 'Stmt', 'elseBranch': 'Stmt'},
        'Print': {'expression': 'Expr'},
        'Return': {'keyword': 'Token', 'value': 'Expr'},
        'Var': {'name': 'Token', 'initializer': 'Expr'},
        'While': {'condition': 'Expr', 'body': 'Stmt'}
    }
    define_ast(output_dir, base_class, types)


def define_expr_classes(output_dir):
    base_class = "Expr"
    types = {
        'Assign': {'name': 'Token', 'value': 'Expr'},
        'Binary': {'left': 'Expr', 'operator': 'Token', 'right': 'Expr'},
        'Call': {'callee': 'Expr', 'paren': 'Token', 'arguments': 'list[Expr]'},
        'Get': {'object': 'Expr', 'name': 'Token'},
        'Grouping': {'expression': 'Expr'},
        'Literal': {'value': 'object'},
        'Logical': {'left': 'Expr', 'operator': 'Token', 'right': 'Expr'},
        'Set': {'object': 'Expr', 'name': 'Token', 'value': 'Expr'},
        'Super': {'keyword': 'Token', 'method': 'Token'},
        'This': {'keyword': 'Token'},
        'Unary': {'operator': 'Token', 'right': 'Expr'},
        'Variable': {'name': 'Token'}
    }
    define_ast(output_dir, base_class, types)


def main():
    if len(sys.argv) != 2:
        print('Usage: python GenerateAst.py <output dir>')
        return

    output_dir = sys.argv[1]

    define_expr_classes(output_dir)

    define_stmt_classes(output_dir)


if __name__ == '__main__':
    main()
