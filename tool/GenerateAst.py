import sys

def defineType(file, base_name: str, class_name: str, fields: list):
    file.write(f'class {class_name}({base_name}):\n')

    file.write(f'\tdef __init__(self, ')
    for name, type in fields:
        file.write(f'{name}: {type}, ')
    file.write('):\n')

    for name, _ in fields:
        file.write(f'\t\tself.{name} = {name}\n')
    file.write('\n\n')


def defineVisitor(file, base_name: str, types: dict):
    file.write('class Visitor(ABC):\n')


def defineAST(output_dir: str, base_name: str, types: dict):
    path = f'{output_dir}/{base_name}.py'

    with open(path, 'w') as file:
        file.write('from abc import ABC, abstractmethod\n')
        file.write('from Token import Token\n')
        file.write('\n')
        file.write(f'class {base_name}(ABC): pass\n\n')  # write base class

        defineVisitor(file, base_name, types)  # write visitors

        for class_name, fields in types.items():
            defineType(file, base_name, class_name, fields)

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
