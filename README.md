# PythonLoxInterpreter
Custom interpreter written in Python for the fictional language Lox.

Following the guidance of the excellent materials from Robert Nystrom at https://craftinginterpreters.com/

## Supported Language Features
### See test.lox for examples of each feature
- Comments (//, /* */)
- Print Statements
- Arithmetic operations (+, -, *, /, **)
- Unary operations (-, !)
- Comparison operations (==, !=, <, <=, >, >=)
- Logical operations (and, or)
- Variable Declarations, Assignments, and Access
- Augmented Assignments (+=, -=, *=, /=)
- Increment and Decrement (++, --)
- Variable Scope and Block Statements
- Lists, List Indexing, List Assignment, List Length
- Control Flow (if-else, while, for)
- Native functions (see list below)
- Function declarations and Function Calls
- Closures (with variable capture)
- Recursion
- Classes (class \<name> { \<methods> })
- Inheritance (class \<name> < \<superclass> { \<methods> })
- Superclass methods (super.\<method>())
- Parse Errors (will detect as many as possible at once)
- Interpreter Runtime Errors

## Installation
- Clone the repository:
`git clone https://github.com/Derek-Fox/PythonLoxInterpreter.git`
- Install dependencies:
`pip install -r requirements.txt`
- Install the package: `pip install .`

## Usage
- Run interactive interpreter: `pylox`
- Run interpreter on Lox source file: `pylox <filename>`
