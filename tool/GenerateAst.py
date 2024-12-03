import sys


def define_visitor(f, base_name: str, types: dict):
    f.write(f'class {base_name}Visitor(ABC):\n')
    for class_name in types.keys():
        f.write('\t@abstractmethod\n')
        f.write(f'\tdef visit_{class_name.lower()}_{base_name.lower()}(self, {base_name.lower()}: "{class_name}{base_name}"): pass\n')
    f.write('\n')


def define_type(f, base_name: str, class_name: str, fields: list):
    f.write(f'class {class_name}{base_name}({base_name}):\n')

    f.write(f'\tdef __init__(self, ')
    for name, type in fields:
        f.write(f'{name}: "{type}", ')
    f.write('):\n')

    for name, _ in fields:
        f.write(f'\t\tself.{name} = {name}\n')

    f.write(f'\tdef accept(self, visitor: "{base_name}Visitor"):\n')
    f.write(f'\t\treturn visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n')
    f.write('\n')


def define_base(base_name, f):
    f.write(f'class {base_name}(ABC):\n')
    f.write('\t@abstractmethod\n')
    f.write(f'\tdef accept(self, visitor: "{base_name}Visitor"): pass\n\n')


def write_imports(base_name, f, types):
    f.write('from abc import ABC, abstractmethod\n')
    f.write('from typing import TYPE_CHECKING\n')
    f.write('from Token import Token\n')
    f.write('\n')
    f.write('if TYPE_CHECKING:\n')
    f.write(f'\tfrom {base_name} import ')
    f.write(', '.join([f'{class_name}{base_name}' for class_name in types.keys()]))
    f.write('\n')


def define_ast(output_dir: str, base_name: str, types: dict):
    path = f'{output_dir}/{base_name}.py'

    with open(path, 'w') as f:
        write_imports(base_name, f, types)

        define_visitor(f, base_name, types)

        define_base(base_name, f)

        for class_name, fields in types.items():
            define_type(f, base_name, class_name, fields)


def define_stmt_class(output_dir):
    base_class = 'Stmt'
    types = {
        'Block': [('statements', 'list[Stmt]')],
        'Expression': [('expression', 'Expr')],
        'If': [('condition', 'Expr'), ('thenBranch', 'Stmt'), ('elseBranch', 'Stmt')],
        'Print': [('expression', 'Expr')],
        'Var': [('name', 'Token'), ('initializer', 'Expr')],
        'While': [('condition', 'Expr'), ('body', 'Stmt')]
    }
    define_ast(output_dir, base_class, types)


def define_expr_class(output_dir):
    base_class = "Expr"
    types = {
        'Logical': [('left', 'Expr'), ('operator', 'Token'), ('right', 'Expr')],
        'Assign': [('name', 'Token'), ('value', 'Expr')],
        'Binary': [('left', 'Expr'), ('operator', 'Token'), ('right', 'Expr')],
        'Grouping': [('expression', 'Expr')],
        'Literal': [('value', 'object')],
        'Unary': [('operator', 'Token'), ('right', 'Expr')],
        'Variable': [('name', 'Token')]
    }
    define_ast(output_dir, base_class, types)


def main():
    if len(sys.argv) != 2:
        print('Usage: python GenerateAst.py <output dir>')
        return

    output_dir = sys.argv[1]

    define_expr_class(output_dir)

    define_stmt_class(output_dir)


if __name__ == '__main__':
    main()
