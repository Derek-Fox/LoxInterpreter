# PythonLoxInterpreter
Custom interpreter written in Python for the fictional language Lox.

Following the guidance of the excellent materials from Robert Nystrom at https://craftinginterpreters.com/

## Supported Language Features
### See test.lox for examples of each feature
- Arithmetic operations (+, -, *, /)
  - e.g. `print (1 + 2) * 3 / 4 - 5;`
- Logical operations (and, or)
  - e.g. `print true and false or true;`
- Variable Declarations, Assignments, and Access
  - e.g. `var x = 5;`, `x = 10;`, `print x;`
- Print Statements
  - e.g. `print 5;`, `print "Hello, World!";`
- Comments (//, /* */)
  - e.g. `// This is a comment`, `/* This is a block comment */`
- Lists, List Indexing, List Assignment, List Length
  - e.g. `var list = [1, 2, 3];`, `print list[0];`, `list[0] = 5;`, `print length(list);`
- Control Flow (if-else, while, for)
  - e.g. `if (x < 5) { print "x is less than 5"; } else { print "x is greater than or equal to 5"; }`
  - e.g. `while (x < 5) { print x; x = x + 1; }`
  - e.g. `for (var i = 0; i < 5; i = i + 1) { print i; }`
- Function declarations and Function Calls
  - e.g. `fun add(a, b) { return a + b; }`, `print add(5, 10);`
- Closures
  - e.g. `fun makeCounter() { var i = 0; fun count() { i = i + 1; return i; } return count; }`
- Recursion
- Classes (class \<name> { \<methods> })
- Inheritance (class \<name> < \<superclass> { \<methods> })
- Superclass methods (super.\<method>())
- 

## Installation
- Clone the repository:
`git clone https://github.com/Derek-Fox/PythonLoxInterpreter.git`
- Install dependencies:
`pip install -r requirements.txt`
- Install the package: `pip install .`

## Usage
- Run interactive interpreter: `pylox`
- Run interpreter on Lox source file: `pylox <filename>`
