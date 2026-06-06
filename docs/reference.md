# Pylem Reference

*Version 0.1 (Draft)*

__The Pylem programming language__ is a dialect of Python but less abstract and more low-level like C. There's a gap in the coding landscape. Projects like [*Mojo*](https://mojolang.org/), [*Cython*](https://cython.org/), and Rust's [*PyO3*](https://pyo3.rs/v0.28.3/) prove there is a massive demand for solving the *two-language problem.* Python is a widely used programming language, but its slow and not meant for performance-critical tasks. That's why many libraries use FFI with compiled code — often written in C — to overcome this limitation. But then you need to write a library in 2 or more languages. Pylem aims to fix that. Python developers won't have to abandon a familiar syntax to write performance-critical code. Pylem will be able to be interpreted and compiled, all within the same language.

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

The first major difference is in the keyword `mut`. Variables are immutable by default. Use `mut` to allow a variable to be mutated. *See [Mutability](#mutability).*

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

Certain keywords can start *blocks* after a colon `:` and a line break. This starts a whitespace sequence with a child scope. Indentation determines when a block ends. Use `pass` to leave a block empty. Lambda functions can have implicit returns from within blocks, with the last expression evaluated in a lambda body being its return value.

```py
block:
    body

block:
    pass
```

### Dual Whitespace-Bracket System

Lambda functions can start a whitespace block when there's a line break after its colon (`:`). When indention is less than the first line in the block, the lambda function ends and parsing returns to expression mode. 

```py
api_call(lambda result:
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

These are immutable variables. Although it might look like it, setting the variable again does not mutate the variable. Each `=` operation is a new variable being declared, a concept known as *shadowing.*

```py
a = 1
a = 2
a = 'a'
```

### Mutability

Mutable variables are declared with the keyword `mut` before the name. Any `=` operation or any compound assignment operators such as `+=` or `-=` will mutate the variable.

```py
mut i: int = 0
i = 1
i += 1
i -= 1
```

There is a chance that instead of mutating, you accidentally declare a new variable since you typo'd the name of it, creating a silent bug. This issue isn't new to Python developers, and so it carries over into Pylem as well. 

```py
mut number = 4

nubmer = 5  # Oops!

print(f"{number}")  # It's still 4!
```

The walrus operator `:=` and any compound assignment operator require that the left-hand side be a mutable reference. You can optionally use that instead of `=` to mitigate this issue.

```py
mut number = 4

nubmer := 5  # Error: "nubmer" is undefined
number := 5  # Fixed!
```

[TOC](#table-of-contents)

---

## Functions

Functions are defined with `def` like in Python. Types are inferred if they're omitted.

```py
def is_thirteen(x):
    if x == 13:
        return True
    return False
```

```py
def fib(n):
    if n < 1:
        return 0
    elif n < 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)
```

Functions declared this way are visible to other functions in the scope no matter what order. They can be overloaded with new declarations of the same name. Overloaded functions are dispatched to the scope that they're defined in.

```py
def divide(a: int, b: int) -> int:
    return a // b

def divide(a: float, b: float) -> float:
    return a / b

divide(5, 2)       # Result: 2
divide(5.0, 2.0)   # Result: 2.5
```

### Lambda Functions

```py
# Function that takes another function as an argument
def apply_operation(value, operation_callback):
    return operation_callback(value)

# Passing a quick square operation as a callback
result = apply_operation(4, lambda x: x ** 2)
print(result)  # Output: 16
```

Lambdas work in Pylem like they do in Python. In addition to the usual syntax of `lambda a, b, c:`, they can also be defined with a name and types like `lambda f(a: T, b: T, c: T) -> T:` by adding parentheses around the parameters, similar to the format for `def` functions.

Lambda functions can be assigned to a variable. Unlike `def` functions, a function defined with `lambda` cannot be overloaded. It's a function pointer that holds a single function. The last expression in a lambda is its implied return value. Lambdas are the only function type with implicit returns since they can be inlined like for example `lambda x: x`.

```py
add_one = lambda x: x + 1
# Or
lambda add_one(x):
    x + 1
```

Even when inside an expression, a lambda function can start a block. If its inside brackets, then exiting the block will return to parsing the rest of the expression.

```py
api_call(lambda result:
    if result > 0:
        print(f"Success! {result}")
    else:
        print(f"Failure! {result}")
)
```

```py
start_countdown(lambda count(n):
    if n > 0:
        print(f"{n}!")
        count(n - 1)
    else:
        print(f"Go!")
, 10)
```

When you define a lambda function in an expression by itself, the function will be assigned to a variable with its name in that scope. In other words, saying `lambda name(x): x` is the same as `name = lambda name(x): x`.

```py
lambda callback(result):
    if result > 0:
        print(f"Success! {result}")
    else:
        print(f"Failure! {result}")

# `callback` is a function pointer in this scope.

api_call(callback)
```

[TOC](#table-of-contents)

---

## Constants

**Constants** are declared with `const`. This marks compile-time data, different from an immutable variable. The variable is treated as if it where a literal. The type can be inferred.

```py
const PI: float = 3.14159265
const NAMESPACE = "development"
```

Constants can have arguments like functions to make **compile-time functions.** These functions are like `def` ones but run at compile time. It uses an explicit return like with `def` functions. 

```py
const MAX(a: int, b: int) -> int:
    if a > b:
        return a
    else:
        return b

MAX(5, 10)    # Result: 10
MAX(7, 3)     # Result: 7
```

[TOC](#table-of-contents)

---

## Control Flow

1. __[`block`](#block)__
2. __[`if`/`elif`/`else`](#if--elif--else)__
3. __[`for`/`in`](#for--in)__
4. __[`while`](#while)__
5. __[`break`/`continue`](#break--continue)__
6. __[`match`/`case`](#match--case)__
7. __[`try`/`except`](#try--except)__
8. __[`return`](#return)__

[TOC](#table-of-contents)

### `block`

A block of code that runs only once, creating a new scope.

```py
block:
    x = 1
    print(f"x = {x}")
```

`block` can have a label after it to call with `break`. If the colon is omitted, then there needs to be another block type after it (for example a `for` loop) and then `break` or `continue` can be applied to that specific block.

```py
block label:
    if cond:
        break label
    print("Condition failed")
```

```py
block outer
for x in range(0, 100):
    for y in range(0, 100):
        if x * y >= 100:
            print(f"{x} * {y} == {x * y}")
            continue outer
        if x * y == 77:
            print("break")
            break outer
```

When the colon is omitted, the label goes to the next non-empty line below `block` which needs to be another block type. Optionally, you can also put it on the same line like `block outer for ....`.

_[Control Flow](#control-flow)_

### `if` / `elif` / `else`

```py
if cond:
    body
elif cond:
    body
else:
    body

expr if cond else expr

expr if cond else expr if cond else ...
```

Basic Boolean branching.

```py
x = x if x > 0 else -x

if x > 0:
    print("positive")
else:
    print("non-positive")
```

Use `and`/`or` to compare multiple booleans at once.

```py
a = True
b = False

if a and b:           # True and False == False
    print("This will not print")
elif a or b:          # True or False == True
    print("This will print")
```

_[Control Flow](#control-flow)_

### `for` / `in`

_[Control Flow](#control-flow)_

### `while`

_[Control Flow](#control-flow)_

#### `break` / `continue`

Control the iteration of a loop

```py
# Stopping a search when an item is found
fruits = ["apple", "banana", "cherry", "date"]

for fruit in fruits:
    if fruit == "cherry":
        print("Found it!")
        break  # Completely stops the loop
    print(f"Checking {fruit}...")

print("Loop finished.")
```

```py
# Skipping specific numbers in a sequence
for num in range(1, 6):
    if num == 3:
        continue  # Skips the rest of this iteration
    print(f"Processing number {num}")

print("Loop finished.")
```

```py
# Simulating a user login or command prompt
while True:
    user_input = input("Enter 'quit' to exit: ")
    if user_input.lower() == 'quit':
        print("Exiting program.")
        break  # Stops the infinite loop immediately
    print(f"You typed: {user_input}")

print("Loop finished.")
```

```py
# Printing odd numbers only
mut count = 0

while count < 5:
    count += 1  # Increment happens BEFORE continue
    if count == 3:
        continue  # Skips printing the number 3
    print(f"Count is: {count}")

print("Loop finished.")
```

_Output:_

```
Count is: 1
Count is: 2
Count is: 4
Count is: 5
Loop finished.
```


Both accept an optional label to target an outer block

```py
block loop1
for i in range(0, 3):
    for j in range(0, 3):
        if i == 1 and j == 1:
            # Skip the rest of the inner loop and jump to the next iteration of loop1
            continue loop1
        print(f"i = {i}, j = {j}")
```

```py
mut x: int
block label:
    if cond then
        x = 5
        break block
    x = 4

print("{x}")     # Prints either "4" or "5"
```

_[Control Flow](#control-flow)_

### `match` / `case`

```py
match expr:
    case ptrn as var:
        body
    case ptrn:
        body
    case _:
        body
```

The `match`/`case` statement acts like a more powerful version of a traditional `switch`/`case` statement found in other languages. It allows you to match values, unpack structures, and filter patterns cleanly without writing long `if`/`elif`/`else` blocks.

This example checks the value of `status_code` and executes the code block under the first matching case. The underscore (`_`) acts as a wildcard *(or else)* to handle any unmatched cases.

```py
def check_status(status_code):
    match status_code:
        case 200:
            return "Success"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:  # Wildcard / Default fallback
            return "Unknown Status"

print(check_status(200))  # Output: Success
print(check_status(999))  # Output: Unknown Status
```

You can use the pipe symbol (`|`) to match multiple conditions inside a single case statement.

```py
enum Role:
    Admin
    Manager
    Guest
    User
    Subscriber
    Billing
    Support

def get_user_role(role: Role):
    match role:
        case Admin | Manager:  # Matches either admin OR manager
            return "Full Access Granted"
        case Support:
            return "Limited Access Granted"
        case _:
            return "Access Denied"
```

You can append an if statement to a case pattern. This is called a **guard,** and it will only enter the case if the pattern matches and the if condition evaluates to `True`.

```py
def process_login(user_info):
    match user_info:
        # Matches a 2-item list/tuple and assigns variables
        case (username, status) if status == "banned":
            return f"Access Denied. {username} is suspended."
        case (username, "active"):
            return f"Welcome back, {username}!"
        case _:
            return "Invalid login format."

print(process_login(("Alice", "banned")))  # Output: Access Denied. Alice is suspended.
print(process_login(("Bob", "active")))    # Output: Welcome back, Bob!
```

`match`/`case` is highly useful for structural pattern matching, such as verifying and extracting specific keys from a dictionary.

```py
def handle_api_response(response):
    match response:
        # Matches if 'error' key exists, extracts its value into 'msg'
        case {"status": "fail", "error": msg}:
            return f"Error occurred: {msg}"
        # Matches if 'data' key exists, extracts its value into 'payload'
        case {"status": "success", "data": payload}:
            return f"Data received: {payload}"
        case _:
            return "Malformed data structure."

print(handle_api_response({"status": "fail", "error": "Timeout"})) # Output: Error occurred: Timeout
```

_[Control Flow](#control-flow)_

### `try` / `except`

```py
try:
    body
except exc as var:
    body
except exc:
    body
except _:
    body
finally:
    body
```

A `try`/`except` block is used to handle runtime errors so that your program does not crash when it encounters an issue.

The `try` block contains the risky code, and the `except` block handles a specific error if it occurs.

```py
try:
    result = 10 / 0  # This raises a ZeroDivisionError
except ZeroDivisionError:
    print("Error: You cannot divide a number by zero!")
```

```py
try:
    # 1. Ask the user for a number
    user_input = input("Enter a number to divide 100 by: ")
    number = int(user_input)  # Might raise ValueError if input is text
    
    # 2. Perform the division
    result = 100 / number     # Might raise ZeroDivisionError if input is 0
except ValueError:
    # Runs if the user types something like "hello"
    print("Error: That is not a valid integer!")
except ZeroDivisionError:
    # Runs if the user types "0"
    print("Error: You cannot divide by zero!")
else:
    # Runs ONLY if the code in the 'try' block succeeds perfectly
    print(f"Success! The result is: {result}")
finally:
    # ALWAYS runs, regardless of whether an error occurred or not
    print("Thank you for using the calculator.")
```

#### `raise`

_[Control Flow](#control-flow)_

### `return`

_[Control Flow](#control-flow)_

[TOC](#table-of-contents)

---

## Types

__[Built-in Types](#built-in-types)__ / __[Custom Types](#custom-types)__

[TOC](#table-of-contents)

### Built-in Types

1. __[Booleans](#booleans-bool)__
2. __[Numbers](#numbers)__
3. __[Characters](#characters-chr)__
4. __[Strings](#strings-str)__
5. __[Lists](#lists-list)__
6. __[Dictionaries](#dictionaries-dict)__
7. __[Tuples](#tuples)__
8. __[None-ables](#none-ables-)__
9. __[Pointers](#pointers-)__

_[Types](#types)_

#### Booleans (`bool`)

`bool` is a built-in enum type with its only variants being `False` and `True`. 

```py
match value:
    case True:
        print("It's true!")
    case False:
        print("It's false!")
```

```py
if value:
    print("It's true!")
else:
    print("It's false!")
```

_[Built-in Types](#built-in-types)_

#### Numbers

_[Built-in Types](#built-in-types)_

#### Characters (`chr`)

Python doesn't have a built-in character type like `char` in C. By default, both single (`'`) and double (`"`) quotes will make strings in Pylem just like they do in Python. You can declare a variable as `chr` and it will expect a string literal of one character or an expression that returns a `chr`. If you set it to a string that isn't 1 character, you will get a compile-time error.

```py
a: chr = 'a'
b: chr = "b"
c = chr(99)  # ASCII value of 'c'
```

Some expressions expect a character, like the input of a function with type `chr`. When a `chr` type is expected, a single-character string literal is automatically interpreted as a `chr`. A literal of more than one character in that context is a compile-time error.

```py
def print_chr(c: chr):
    print(str(c))

print_chr("c")   # OK
print_chr("cd")  # Error!
```

Some expressions will return a `chr` like indexing or looping a string.

```py
s = "hello"
print(isinstance(s[0], chr))

for c in s:
    print(f"'{c}' is a chr? {isinstance(c, chr)}")
```

Without a `chr` context, a single-character string literal is still a `str` as normal. So `x = 'a'` gives a `str`, but `x: chr = 'a'` or `x = 'a'[0]` gives a `chr`. That distinction is what makes `print_chr("c")` work while `s = "c"; print_chr(s)` would not — unless `s` was itself declared as `chr`.

_[Built-in Types](#built-in-types)_

#### Strings (`str`)

_[Built-in Types](#built-in-types)_

#### Lists (`list`)

_[Built-in Types](#built-in-types)_

#### Dictionaries (`dict`)

_[Built-in Types](#built-in-types)_

#### Tuples

_[Built-in Types](#built-in-types)_

#### None-ables (`?`)

In Python, it's common to set things to `None` if you haven't set it yet. This works in dynamically typed languages, but Pylem is statically typed. To make this work, some values can be set to `None` if its type is declared with a question mark `T?`. This must be checked for `None` before using.

```py
x: int? = get_number()

if x != None:
    # x is safe here
    print(f"The number is {x}")
else:
    print("No number")
```

Internally, what's happening is that the value becomes a tagged union with 2 variants: *`Some` value* or `None`. *(See [`enum union`](#enum-union).)* When you enter a block where it's guaranteed not to be `None`, then it's automatically unwrapped inside that block.

You can kind of think of it as doing something like this under the hood:

```py
enum union OptionInt:
    Some: int
    None

x: OptionInt = get_number()

match x:
    case Some as x_val:
        print(f"The number is {x_val}")
    case None:
        print("No number")
```

If an enum or tagged union is None-able, then `None` becomes one of its variants.

```py
answer: bool? = get_answer()

match answer:
    case True:
        print("Yes")
    case False:
        print("No")
    case None:
        print("Maybe")
```

```py
enum union Payload:
    Integer: int
    Float: float

payload: Payload? = get_payload()

match payload:
    case Integer as val:
        print(f"Got an integer: {val}")
    case Float as val:
        print(f"Got a float: {val}")
    case None:
        print("Payload is empty")
```

_[Built-in Types](#built-in-types)_

#### Pointers (`*`)

_[Built-in Types](#built-in-types)_

### Custom Types

1. __[`struct`](#struct)__ — *Structured Data*
2. __[`enum`](#enum)__ — *Enumerated Data*
3. __[`union`](#union)__ — *Untagged Unions*
4. __[`enum union`](#enum-union)__ — *Tagged Unions*
5. __[`class`](#class)__ — *Virtual Interfaces*

_[Types](#types)_

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

_[Custom Types](#custom-types)_

#### `enum`

Enums contain a set of fixed values, typically 1 byte each. The size of an enum is the size of its largest variant. By default, this is a single byte if there are fewer than 256 variants, but they can also be assigned other values such as integers which can increase the size of the enum. When assigning a variant with a specific value, the variants that follow it will iterate from the previous one. Each variant must have a unique value.

```py
enum Direction:
    UP
    DOWN
    LEFT
    RIGHT

enum Color:
    RED = 0xFF0000
    BLUE = 0x00FF00
    GREEN = 0x0000FF

dir = Direction.UP
color = Color.RED
```

Enums are often paired with `match` to switch to multiple branches based on its value. Each `case` only needs the name of each variant based on the type passed to `match`.

```py
match dir:
    case UP:
        print("Go up!")
    case DOWN:
        print("Go down!")
    case LEFT:
        print("Go left!")
    case RIGHT:
        print("Go right!")
```

To attach data to an enum, use `enum union`:

```py
enum union MyTaggedUnion:
    First
    Second: int
    Third: {val: int}

a = MyTaggedUnion.First
b = MyTaggedUnion.Second(2)
c = MyTaggedUnion.Third(val=3)
```

*See [`enum union`](#enum-union) for more information.*

_[Custom Types](#custom-types)_

#### `union`

**Untagged unions** – sometimes known as *sum types* – can be defined with the keyword `union`. Define each member like a struct. If the type is omitted, then the name is the type (for example `int` means `int: int`). Unlike a struct, a union is the size of its largest member. Instantiate a union by naming one of its members in the function call as opposed to naming every member like with structs.

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

_[Custom Types](#custom-types)_

#### `enum union`

Unions can be tagged with an enum to create **tagged unions.** To do this, create an `enum` and then extend it with a `union`. Each member name in the union must match with each varient of the enum. If a variant has no data, assign its type as `void`. Instantiate it by passing in its tag first and then assign the member for that tag if it has data. The size of a tagged union is the size of its enum component and the size of its union component combined.

```py
enum PayloadTag:
    Integer
    Float
    Text
    Tuple
    Empty

union Payload(PayloadTag):
    Integer: int
    Float: float
    Text: str
    Tuple: {val: int}
    Empty: void

payload = Payload(PayloadTag.Integer, Integer=1)
payload = Payload(PayloadTag.Tuple, Tuple={val: 1})
payload = Payload(PayloadTag.Empty)
```

Pattern matching works the same as enums. To get the data of a variant, put `as` after the variant name.

```py
match payload:
    case Integer as val:
        print(f"Got an integer: {val}")
    case Float as val:
        print(f"Got a float: {val}")
    case Text as val:
        print(f"Got text: {val}")
    case Tuple as x:
        print(f"Got a tuple: \{ val: {x.val} }")
    case Empty:
        print("Payload is empty")
```

A union can be tagged with an anonymous enum by declaring it with `enum union`. This blends the concepts of enums and unions together to create a *true sum type* and will allow you to instantiate it with each member as a variant. Varients without data are empty and set to `void`.

```py
enum union MyTaggedUnion:
    First
    Second: int
    Third: {val: int}

a = MyTaggedUnion.First
b = MyTaggedUnion.Second(2)
c = MyTaggedUnion.Third(val=3)
```

```py
match a:
    case First:
        print("first!")
    case Second as val:
        print(f"second! {val}")
    case Third as x:
        print(f"third! {x.val}")
```

_[Custom Types](#custom-types)_

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

__Interfaces:__ an interface is a class without any data. It works like `interface` or `trait` in other languages.

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

__Constructors:__ When a type has one or more `__init__(mut self)` methods defined, you can use that to create the type instead of the standard instantiation method. This can be overloaded to create multiple ways to initiate a type. The first argument `mut self` is an unset reference to the new object. If it's a struct, then all members need to be set. If it's an enum or union, then it must be set to one of its variants.

```py
class BankAccount:
    def __init__(mut self, owner, balance=0):
        self.owner = owner
        self.balance = balance

# Creating an object instance
my_account = BankAccount("Alex", 100)
print(f"{my_account.owner} has ${my_account.balance}")
```

_[Custom Types](#custom-types)_

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

- [`block`](#block), [`case`](#match--case), [`const`](#constants), [`enum`](#enum), [`match`](#match--case), [`mut`](#mutability), [`struct`](#struct), [`union`](#union)

---

*This document captures the current state of the Pylem design. The language is still evolving.*


