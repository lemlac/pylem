# Pylem Reference

*Version 0.1 (Draft)*

__The Pylem programming language__ is a dialect of Python but less abstract and more low-level like C. There's a gap in the coding landscape. Projects like [*Mojo*](https://mojolang.org/), [*Cython*](https://cython.org/), and Rust's [*PyO3*](https://pyo3.rs/v0.28.3/) prove there is a massive demand for solving the *two-language problem.* Python is a widely used programming language, but its slow and not meant for performance critical tasks. That's why many libraries use FFI with compiled code — often written in C — to overcome this limitation. But then you need to write a library in 2 or more languages. Pylem aims to fix that. Python developers won't have abandon a familiar syntax to write performance critical code. Pylem will be able to be interpreted and compiled, all within the same language.

Most things in Pylem will work just like in Python.

```py
print("Hello, World!")
```

```py
name = "Alice"
age = 30

# Using an f-string for formatting
print(f"My name is {name} and I am {age} years old.")
```

```py
score = 85

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
else:
    print("Grade: C")
```

```py
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(f"I like eating {fruit}")
```

```py
# Standard list
numbers = [1, 2, 3, 4, 5]

# List comprehension to square each number
squares = [num ** 2 for num in numbers]
print(squares)  # Output: [1, 4, 9, 16, 25]
```

```py
user_profile = {
    "username": "coder123",
    "email": "coder123@example.com",
    "verified": True
}

# Accessing a value by its key
print(user_profile["email"])
```

```py
def calculate_area(width, height):
    return width * height

room_area = calculate_area(12, 15)
print(f"The room is {room_area} square feet.")
```

Not all Python code works in Pylem, and this document will go through the major differences.

The first major difference is in the keyword `mut`. Variables are immutable by default. Use `mut` to allow a variable to be mutated, and mutate it with the `:=` operator. *See [Assignment](#assignmemt).*

```py
secret_word = "pylem"
mut guess = ""

while guess != secret_word:
    guess = input("Enter the secret word: ").lower()

print("Access granted!")
```

Another key difference is the inclusion of custom data types like in C: `struct`, `enum`, and `union`. *See [Custom Types](#custom-types).*

```py
struct BankAccount:
    owner: str
    balance: int

class BankAccount:
    def __init__(mut self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        
    def deposit(mut self, amount):
        self.balance += amount
        return f"${amount} deposited. New balance: ${self.balance}"

# Creating an object instance
my_account = BankAccount("Alex", 100)
print(my_account.deposit(50))
```

Lambda functions can have multiple lines. Pylem has special rules using a mix of indentation and commas/closing brackets to know when a lambda function ends. *See [Lambda Functions](#lambda-functions).*

```py
# The main function accepting the callback
def calculate_and_report(num1, num2, callback_func):
    total = num1 + num2
    callback_func(total)  # Executing the callback here

# Testing the code with different callbacks
calculate_and_report(5, 7, lambda result:
    print(f"The answer is: {result}")
)
# Output: The answer is: 12

calculate_and_report(
    5,
    7,
    lambda result:
        print(f"✨ SUCCESS! The calculated total is: {result} ✨")
)
# Output: ✨ SUCCESS! The calculated total is: 12 ✨
```

---

## Table of Contents

1. __[Basics](#basics)__
2. __[Assignment](#assignment)__
3. __[Functions](#functions)__
4. __[Constants](#constants)__
5. __[Control Flow](#control-flow)__
6. __[Types](#types)__
7. __[Generics](#generics)__
8. __[Operators](#operators)__
9. __[Advanced](#advanced)__
10. __[Reserved Words](#reserved-words)__

---

## Basics

Comments are done with `#` or with multiline strings `""" … """`

```py
# Comment
"""
Block Comment
"""
```

A program in Pylem is divided into expressions and sequences. Sequences can either be delimited with whitespace and semi-colons (`;`) or brackets and commas (`,`). The default is a whitespace sequence, where each line is an expression. Multiple expressions can be on one line separated by semi-colons (`;`).

```py
expr
expr

expr; expr
```

### Blocks

Certain keywords can start *blocks* after a colon `:` and a line break. This starts a whitespace sequence with a child scope. Indentation determines when a block ends. The last expression evaluated in a block is its value. Use `pass` to leave a block empty.

```py
block:
    body

block:
    pass
```

### Dual Whitespace-Bracket System

Lambda functions can start a whitespace block when there's a line break after its colon (`:`). When indention is less than the first line in the block, the lambda function ends and parsing returns to expression mode. 

```py
apiCall(lambda result:
    if result > 0:
        print(f"Success! {result}")
    else:
        print(f"Failure! {result}")
)
```

### Declarations

Variables are declared with just the equals sign (`=`). A type may be optionally added with a colon (`:`) after the variable name or inferred without it. This type of variable is **immutable.** Additional *assignments* to a variable **shadow** that variable. 

```py
a = 0
b: int = 1
a = 2      # New `a`
b = 3      # New `b`
```

Shadowing works like `let` in other languages. It's just that Pylem drops the `let` all together for the simpler `=` notation like in Python.

Functions are declared with `def`. The return type can be inferred based on the return value, and the types of parameters may be inferred based on usage. This combines the simplicity of dynamic typing with the power and optimization of static typing.

```py
def f(x: int) -> int:
    return x*x
def g(x):
    return x*x*x
f(2)   # Result: 4
g(2)   # Result: 8
```

[TOC](#table-of-contents)

---

## Assignment

Variables can be declared with the equals sign `=`. Type notation uses `: T =` but can be inferred.

```py
a = 0
b: int = 2
```

These are immutable variables. Although it might look like it, setting the variable again does not mutate the variable. Each `=` operation is a new variable being declared, a concept known as**shadowing.**

```py
a = 1
a = 2
a = 'a'
```

Mutable variables are declared with the keyword `mut` before the name. Any `=` operation or any compound assignment operators such as `+=` or `-=` will mutate the variable.

```py
mut i: int = 0
i = 1
i += 1
i -= 1
```

There is a chance that instead of mutating, you accidentally declare a mew variable since you typo'd the name of it, creating a silent bug. This issue isn't new to Python developers, and so it carries over into Pylem as well. 

```py
mut number = 4

nubmer = 5   # Oops!

print(f"{number}")  # It's still 4!
```

[TOC](#table-of-contents)

---

## Functions

### Lambda Functions

```py
def apply_operation(value, operation_callback):
    return operation_callback(value)

# Passing a quick square operation as a callback
result = apply_operation(4, lambda x: x ** 2)
print(result)  # Output: 16
```

Lambdas work in Pylem like they do in Python. In addition to the usual syntax of `lambda a, b, c:`, they can also be defined with a name and types like `lambda f(a: T, b: T, c: T) -> T:` by adding parentheses around the parameter, similar to the format for `def` functions.

[TOC](#table-of-contents)

---

## Constants

[TOC](#table-of-contents)

---

## Control Flow

[TOC](#table-of-contents)

---

## Types

### Custom Types

#### `struct`

Structs are product types—or in other words—plain data containers. They cannot extend other structs. Define a struct with the keyword `struct` and then list each member of it in the block.

```py
struct MyStruct:
    name: str
    value: int
```

Instantiate a struct by calling it like a function. Each member is treated like a named argument.

```py
myObject = MyStruct(name="Foobar", value=1)
```

Structs are transparent. They can be destructured like named tuples. 

```py
struct TransparentThing:
    a: int
    b: int

{a, b} = TransparentThing(a=1, b=2)
print(f"a: {a}, b: {b}")
```

#### `enum`

Enums are sum types. They define a closed set of variants. Variants may carry data turning them into a tagged union. Use the keyword `enum` to define one.

```py
enum MyEnum:
    First
    Second(int)
    Third{val: int}
```

Like structs, instantiate by calling the member like a function unless it doesn't carry any data.

```py
a = MyEnum.First
b = MyEnum.Second(2)
c = MyEnum.Third(val=3)
```

When pattern matching, you only need to name the member of the type in each case, not the full path. Use `_` while destructuring to discard the members data.

```py
match a:
    case First:
        print("first!")
    case Second(_):
        print("second!")
    case Third{_}:
        print("third!")
```

#### `union`

Untagged unions – also called *sum types* – can be defined with the keyword `union`. Define each member like a struct. If the type is ommited, then the name is the type (for example `int` means `int: int`). Unlike a struct, a union is the size of its largest member. Instantiate a union by naming one of its members in the function call as opposed to naming every member like with structs.

```py
union SumUnion:
    int
    float
    char

u = SumUnion(int=1)

u.int     # Value is 1
u.float   # Read binary representation of int 1 as if it were a float
u.char    # Read binary representation of int 1 as if it were a, value is '\1'
```

This is similar to C unions where it doesn't do any conversion; it only reads whatever data is there with a different type. Unions will set overflow data to 0 so that if you set a small member and then read from a big member, you won't get undefined behavior. The zero-padding interacts with endianness in a way that's deterministic but platform-dependent. The behavior is always defined, just not always portable. 

```py
u = SomeUnion(char='\1')   # char (1 byte), remaining bytes zeroed

# Little-endian: memory is [0x01, 0x00, 0x00, 0x00]
u.int          # Value: 1

# Big-endian: memory is [0x01, 0x00, 0x00, 0x00]  (same bytes)
u.int          # Value: 0x01000000 = 16777216
```

#### `class`

Pylem separates data types from virtual classes. Much like `class` in Python, `class` in Pylem defines a set of methods for a type. The main difference is that the type has no data by default. Instead, you define the data structure first (for example with `struct`) and then implement the methods for that data structure under `class` with the same name. `class` in Pylem works like a combination of [`impl`](https://doc.rust-lang.org/std/keyword.impl.html) and [`trait`](https://doc.rust-lang.org/rust-by-example/trait.html) in Rust.

```py
# 1. Define the raw, flat memory layout (no overhead)
struct BankAccount:
    owner: str
    balance: int

# 2. Add methods to that layout (Works like Rust's `impl BankAccount`)
class BankAccount:
    def deposit(mut self, amount: int):
        self.balance += amount
```

__Creating virtual interfaces:__ an interface is a class without any data. It works like `interface` or `trait` in other languages.

```py
# Defines a contract (Works like Rust's `trait Renderable`)
class Renderable:
    def render(self) -> str:
        pass
```

Implement an interface into another class by extending it. Each `class` definition adds new methods to a type, much like how each `def` block of the same function overloads it.

```py
# Implement the 'Renderable' behavior specifically for 'BankAccount'
class BankAccount(Renderable):
    def render(self) -> str:
        return f"Account owner: {self.owner}, Balance: {self.balance}"
```

[TOC](#table-of-contents)

---

## Generics

[TOC](#table-of-contents)

---

## Operators

[TOC](#table-of-contents)

---

## Advanced

[TOC](#table-of-contents)

---

## Reserved Words

The 35 reserved words in Python are also reserved in Pylem:

- `False`, `None`, `True`, `and`, `as`, `assert`, `async`, `await`, `break`, `class`, `continue`, `def`, `del`, `elif`, `else`, `except`, `finally`, `for`, `from`, `global`, `if`, `import`, `in`, `is`, `lambda`, `nonlocal`, `not`, `or`, `pass`, `raise`, `return`, `try`, `while`, `with`, `yield`

There are also new reserved words unique to Pylem:

- `case`, `enum`, `match`, `mut`, `struct`, `union`

---

*This document captures the current state of the Pylem design. The language is still evolving.*
