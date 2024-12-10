# PythonLoxInterpreter
Custom interpreter written in Python for the fictional language Lox.

Following the guidance of the excellent materials from Robert Nystrom at https://craftinginterpreters.com/

## Supported Language Features
#### See test.lox for examples of each feature
- Comments (//, /* */)
- Print Statements
- Arithmetic operations (+, -, *, /, **)
- Unary operations (-, !)
- Comparison operations (==, !=, <, <=, >, >=)
- Logical operations (and, or)
- Variable Declarations, Assignments, and Access
- Augmented Assignments (+=, -=, *=, /=)
- Increment and Decrement (++, --)
- Strings and String Concatenation
- Variable Scope and Block Statements
- Lists, List Indexing, List Assignment, List Length
- Control Flow (if-else, while, for)
- Native functions (see list below)
- Global Math Constants (PI, E)
- Function declarations and Function Calls
- Closures (with variable capture)
- Recursion
- Classes (class \<name> { \<methods> })
- Inheritance (class \<name> < \<superclass> { \<methods> })
- Superclass methods (super.\<method>())
- Parse Errors (will detect as many as possible at once)
- Runtime Errors

### Native Functions
- print(value): Print a value to the console.
- isType(value, type): Check if a value is of a certain type. Returns a boolean.
- convert(value, type): Convert a value to a certain type. Returns the converted value.
- sqrt(value): Return the square root of a number.
- ln(value): Return the natural logarithm of a number.
- log10(value): Return the base 10 logarithm of a number.
- exp(value): Return e raised to the power of a number.
- randFloat(min, max): Return a random float between min and max.
- randInt(min, max): Return a random integer between min and max.
- length(value): Return the length of a list or string.
- input(): Return a string from user input.
- clock(): Return the current time in seconds since the epoch.
- sleep(seconds): Pause execution for a number of seconds.
- exit(code): Exit the interpreter with a status code.

## Installation
- Clone the repository: `git clone https://github.com/Derek-Fox/pylox.git`
- Navigate to repository: `cd pylox`
- Install dependencies: `pip install -r requirements.txt`
- Install the package: `pip install .`

## Usage
- Run interactive interpreter: `pylox`
- Run interpreter on Lox source file: `pylox <filename>`
