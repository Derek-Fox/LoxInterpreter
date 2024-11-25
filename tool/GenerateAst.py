import sys


def defineType(f, base_name: str, class_name: str, fields: list):
    f.write(f'class {class_name}({base_name}):\n')

    f.write(f'\tdef __init__(self, ')
    for name, type in fields:
        f.write(f'{name}: {type}, ')
    f.write('):\n')

    for name, _ in fields:
        f.write(f'\t\tself.{name} = {name}\n')

    f.write(f'\tdef accept(self, visitor: Visitor):\n')
    f.write(f'\t\tvisitor.visit(self)\n')
    f.write('\n')


def defineVisitor(f, base_name: str, types: dict):
    f.write('class Visitor(ABC):\n')
    for class_name in types.keys():
        f.write('\t@abstractmethod\n')
        f.write(f'\tdef visit{class_name}{base_name}(self, expr: {class_name}): pass\n')
    f.write('\n')


def defineAST(output_dir: str, base_name: str, types: dict):
    path = f'{output_dir}/{base_name}.py'

    with open(path, 'w') as f:
        f.write('from abc import ABC, abstractmethod\n')
        f.write('from Token import Token\n')
        f.write('\n')
        f.write(f'class {base_name}(ABC):\n')
        f.write('\t@abstractmethod\n')
        f.write('\tdef accept(self, visitor: Visitor): pass\n')

        defineVisitor(f, base_name, types)  # write visitors

        for class_name, fields in types.items():
            defineType(f, base_name, class_name, fields)


def main():
    if len(sys.argv) != 2:
        print('Usage: python GenerateAst.py <output dir>')
        return

    output_dir = sys.argv[1]
    types = {  # Subtype name: [fields: (field, type)]
        'Binary': [('left', 'Expr'), ('op', 'Token'), ('right', 'Expr')],
        'Grouping': [('expr', 'Expr')],
        'Literal': [('value', 'object')],
        'Unary': [('op', 'Token'), ('right', 'Expr')],
    }
    base_class = "Expr"

    defineAST(output_dir, base_class, types)


if __name__ == '__main__':
    main()
