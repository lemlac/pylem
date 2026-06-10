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
    def __init__(mut self: ptr, owner, balance=0):
        self.owner = owner
        self.balance = balance
        
    def deposit(mut self: ptr, amount):
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
7. __[Operators](#operators)__
8. __[Advanced](#advanced)__
9. __[Reserved Words](#reserved-words)__

_[Top](#pylem-reference)_

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

There isn't a good way to *fix* this issue. The problem is just in the inherent design of Python's declaration system. You can't fix that without significantly changing from Python's core design. You can't just catch typos because `nubmer` could be any variable name. To the compiler, `nubmer` isn't a typo; it's a perfectly valid, newly declared immutable identifier. Because Python's syntax says that *any unbound name on the left side of an `=` is a new variable,* Pylem's compiler has absolutely no way to know whether you meant to modify `number` or if you legitimately wanted to spin up a brand new variable named `nubmer`. This is the trade-off for making Pylem still feel *Pythonic.*

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

*For more on that, see [Compile-time Functions](#compile-time-functions).*

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
8. __[`with`](#with)__
9. __[`return`](#return)__
10. __[`defer`](#defer)__

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

Can we apply this to loops? If you try to call `continue` on a block, you'll get a syntax error since `block` isn't a loop.

```py
block outer:
    for x in range(0, 100):
        for y in range(0, 100):
            if x * y >= 100:
               print(f"{x} * {y} == {x * y}")
               continue outer    # SyntaxError
            if x * y == 77:
                print("break")
                break outer
```


Here `continue` would be being applied to a `block`, not a label to a `for` loop. `block`s aren't loops, so `continue` wouldn't make any sense. The problem with ending with a colon here is that it implies it's creating a new block rather than modifying the next block. 

Instead we can omit the colon (`:`) and put the loop on the same line. This indicates that we want to apply a label to the following block rather than creating a new one.

```py
block outer for x in range(0, 100):
    for y in range(0, 100):
        if x * y >= 100:
            print(f"{x} * {y} == {x * y}")
            continue outer
        if x * y == 77:
            print("break")
            break outer
```

When the colon is omitted, another block type is expected such as `for` or `while`. You can optionally split the label to its own line using `\` too.

```py
block outer \
for x in range(0, 100):
    for y in range(0, 100):
        if x * y >= 100:
            print(f"{x} * {y} == {x * y}")
            continue outer
        if x * y == 77:
            print("break")
            break outer
```

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

Iterates through a list of items:

```py
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

*Output:*

```
apple
banana
cherry
```

* The Iterable Sequence: `fruits` is the list containing the items you want to step through.
* The Loop Variable: `fruit` acts as a placeholder that automatically takes the value of the current item during each iteration.
* The Colon (`:`): Signifies the start of the loop body.
* Indentation: The indented code under the for statement defines what actions execute on every item.

If you need to repeat an action a specific number of times, pair the loop with the built-in `range()` function: 

```py
# Generates numbers from 0 to 4
for i in range(5):
    print("Iteration:", i)
```

Strings (`str`) are iterable collections of single characters (`chr`):

```py
for letter in "Pylem":
    print(str(letter))
```

Use `enumerate()` if you need to track the position index of each item as you loop:

```py
colors = ["red", "green", "blue"]
for index, color in enumerate(colors):
    print(f"Index {index} is {color}")
```

_[Control Flow](#control-flow)_

### `while`

A `while` loop repeats a block of code as long as a specific condition remains true.

```py
# Initialize the counter variable
mut count = 1
# The loop runs as long as count is less than or equal to 5
while count <= 5:
    print(f"The count is: {count}")
    # Increment the counter to eventually end the loop
    count += 1

print("Loop finished!")
```

*Output:*

```
The count is: 1
The count is: 2
The count is: 3
The count is: 4
The count is: 5
Loop finished!
```

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
    if cond:
        x = 5
        break label
    x = 4

print(f"{x}")     # Prints either "4" or "5"
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

#### Pattern Fallback

If a pattern can't be **guaranteed** for any reason, then you must have a **fallback:**

- __Optional binding:__ `Pattern as x?` — wraps `x` in type None-able `T?`

You can have multiple patterns match to one case. If any of the patterns destructure with a variable, the same variable name and type must be in all patterns. If not, omit `as` or use a wildcard `(_)` in each pattern.

```py
match choice:
    case First:
        print("First")
    case Second as val | Third as {val}:  # `val` must be in all patterns
        print(f"Second or Third, val={val}")
```

```py
# `First` doesn't have any values, so destructuring must be disabled.
match choice:
    case First | Second | Third:
        print("First, Second, or Third")
```

```py
# Fallback, `val` is converted to question type `T?`:
match choice:
    case First | Second as val? | Third as {val}?:
        print(f"First, Second, or Third: {val ?? "None"}")
```

```py
match choice:
    case First | Second as val? | Third as {val}?:
        val = val ?? "None"   # Defaults to "None" for the rest of the block
        print(f"First, Second, or Third: {val}")
```

#### `fallthrough`

Proceeds to the next case, which must not destructure new values, unless fallbacks are used. Any case that doesn't have `fallthrough` will break the `match`. This reverses the standard `switch` schematic but allows you to still opt into it where necessary. 

```py
match choice:
    case First:
        print("First")
        fallthrough
    case Second as x?:  # `?` in pattern wraps the variable in a None-able type
        if x is not None:
            print("Definitely Second: {x}")
    # Implicit break.
    case _:
        print("No match")
```

`fallthrough` only goes to the next case. If the next case doesn't have a `fallthrough` in it too, then it will break. It's a syntax error if you call `fallthrough` on the last case in the `match` block.

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
else:
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

The `raise` keyword manually triggers an exception to stop program execution when a specific condition occurs. You can use raise alongside standard built-in exceptions (like `ValueError` or `TypeError`) and include a descriptive error message.

```py
def set_age(age):
    if age < 0:
        # Trigger an error for invalid data
        raise ValueError("Age cannot be negative!")
    print(f"Age successfully set to {age}")
# This will trigger the exception
set_age(-5)
```

Output:

```
Traceback (most recent call last):
  File "script.pyl", line 7, in <module>
    set_age(-5)
  File "script.pyl", line 4, in <module>
    raise ValueError("Age cannot be negative!")
ValueError: Age cannot be negative!
```

Sometimes you want to catch an error to log it or run clean-up code, but still let the error pass up to the main program. Calling `raise` without arguments re-throws the current active exception.

```py
def calculate_payout(amount, people):
    try:
        return amount / people
    except ZeroDivisionError:
        print("Log: Attempted to divide by zero group members.")
        raise # Re-raises the ZeroDivisionError
try:
    calculate_payout(100, 0)
except ZeroDivisionError:
    print("Main Program: Cannot split money among 0 people.")
```

You can define your own specialized error types by creating a class that inherits from the base `Exception` class.

```py
# Define the custom exception
class InsufficientFundsError(Exception):
    pass
def withdraw_money(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(f"You tried to withdraw ${amount} but only have ${balance}.")
    return balance - amount
# Test the custom exception
try:
    withdraw_money(50, 100)
except InsufficientFundsError as error:
    print(f"Transaction Denied: {error}")
```

_[Control Flow](#control-flow)_

### `with`

The `with` statement is used for automatic resource management. It ensures that resources like files, locks, or database connections are properly cleaned up and closed after use, even if your code encounters an error or crashes.

This is the most common use case. The file automatically closes when code leaves the with block, eliminating the need to call `file.close()` manually.

```py
# Example 1: Writing to a file
with open("example.txt", "w") as file:
    file.write("Hello, Python!")
# Example 2: Reading from a file
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
```

You can manage multiple resources simultaneously by separating them with commas. This is ideal for tasks like copying data from one file to another.

```py
# Copying content from a source file to a destination file
with open("source.txt", "r") as source, open("destination.txt", "w") as dest:
    dest.write(source.read())
```

The with block simplifies thread synchronization. It automatically acquires the lock when entering the block and releases it when exiting.

```py
import threading
lock = threading.Lock()
with lock:
    # The lock is automatically acquired here
    print("This code is thread-safe!")
    # The lock is automatically released here
```

Objects that work with a with statement are called context managers. You can create your own by using a class with `__enter__()` and `__exit__()` methods. *(See [Dunder Methods](#dunder-methods).)*

```py
class DatabaseConnection:
    def __enter__(self: ptr):
        print("Connecting to the database...")
        return "Connection_Object"
    def __exit__(self: ptr, exc_type, exc_val, exc_tb):
        print("Closing the database connection safely.")
        # Returning True would swallow exceptions; returning None/False propagates them

# Using the custom context manager
with DatabaseConnection() as db:
    print(f"Executing queries using: {db}")
```

_[Control Flow](#control-flow)_

### `return`

The `return` statement is used inside a function to exit it and pass a value back to the place where the function was called.

```py
def add_numbers(a, b):
    return a + b  # Sends the sum back to the caller
# Call the function and store the result in a variable
total = add_numbers(5, 3)

print(total)  # Output: 8
```

__Key Rules of `return`:__

* __Exits immediately:__ Any code written after the return statement inside the same block is completely ignored.
* __Returns `void` by default:__ Unlike Python, void functions in Pylem do not return `None` by default and cannot be used within an expression. They must be in their own expression by themselves.

You can return more than one value by separating them with commas. They'll be grouped into a tuple, which you can easily unpack:

```py
def get_user_profile():
    name = "Alice"
    age = 30
    return name, age  # Returns a tuple: ("Alice", 30)
# Unpack the two returned values into separate variables
user_name, user_age = get_user_profile()

print(user_name)  # Output: Alice
print(user_age)   # Output: 30
```

_[Control Flow](#control-flow)_

### `defer`

The `defer` keyword delays the execution of a function until the surrounding function returns. It is commonly used for resource cleanup, unlocking files, and managing application panics. It has some overlap with the `with` block but aimed to make it easier to transition from C code where a `goto` statement might be used for the same purpose. 

A deferred function call is pushed onto a stack. The program executes everything else in the function first, then runs the deferred code at the very end.

```py
def defer_example_print():
    # This is scheduled to run last
    defer print("Goodbye") 
    print("Hello")

defer_example_print()
# Output:
# "Hello"
# "Goodbye"
```

`defer` makes it possible to do things that are possible in C but not Python without needing to implement `goto`.

```c
// Source - https://stackoverflow.com/a/245761
// Posted by Greg Rogers, modified by community. See post 'Timeline' for change history
// Retrieved 2026-06-09, License - CC BY-SA 3.0

void foo()
{
    if (!doA())
        goto exit;
    if (!doB())
        goto cleanupA;
    if (!doC())
        goto cleanupB;

    /* everything has succeeded */
    return;

cleanupB:
    undoB();
cleanupA:
    undoA();
exit:
    return;
}
```

```py
def foo():
    if not doA():
        return
    if not doB():
        defer undoA()
    if not doC():
        defer undoB()
	# everything has succeeded
```

__Unlocking Mutexes (Concurrency):__ When writing concurrent code with shared resources, you must unlock your mutexes. Putting `defer mu.unlock()` right after `mu.lock()` prevents unexpected deadlocks if your function returns unexpectedly.

```py
from sync import Mutex

struct Counter:
	mu: Mutex
	value: int

class Counter:
    increment(mut self: ptr):
    	self.mu.lock()
    	defer self.mu.unlock() # Guaranteed to unlock when increment() finishes
    	self.value += 1
```

__Multiple Defers (LIFO Order):__ If you use multiple `defer` statements in a single function, they'll be execute in *Last-In, First-Out* (LIFO) order (a stack structure).

```py
def defer_example_lifo():
    defer print("First Defer Statement")
    defer print("Second Defer Statement")
    defer print("Third Defer Statement")
    print("Main logic runs here")

defer_example_lifo()
# Output:
# "Main logic runs here"
# "Third Defer Statement"
# "Second Defer Statement"
# "First Defer Statement"
```

__Immediate Argument Evaluation:__ A common point of confusion is when arguments inside a defer statement are calculated. Arguments are evaluated immediately when the `defer` line is reached, not when the function finally runs.

```py
def defer_evaluation_example():
	mut x = 10
	# x is evaluated to 10 right here
	defer print(f"Value in defer: {x}") 
	x := 20
	print(f"Value in main: {x}")

defer_evaluation_example()
# Output:
# "Value in main: 20"
# "Value in defer: 10"
```

__`defer` blocks:__ Instead of a function call, add a colon (`defer:`). This is a more generic approach that behaves closer to C's `goto`.

```py
defer:
    final_score += 5

defer:
    undoB()
    undoA()
```

- **`defer f(x)`** — function call form, arguments evaluated immediately
- **`defer: block`** — block form, everything evaluated at return time, no ambiguity

Since real cleanup often involves multiple statements, the block form maps naturally to the C `goto` cleanup pattern.

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
5. __[Arrays](#arrays-arr--list)__
6. __[Dictionaries](#dictionaries-dict)__
7. __[Tuples](#tuples)__
8. __[None-ables](#none-ables-)__
9. __[Pointers](#pointers-ptr)__
10. __[Dynamic Type](#dynamic-type-dyn)__

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

The three basic numbers in Python are also available in Pylem: integers (`int`), floating-point numbers (`float`), and complex numbers (`complex`). Variables automatically take on these types when you assign a numeric value to them. 

| Type | Description | Code Example |
|:---|:---|:---|
| `int` | Positive or negative whole numbers without decimals. | `x = 42` |
| `float` | Real numbers containing one or more decimals or exponential scientific notation. | `y = -3.14` |
| `complex` | Numbers written with a real part and an imaginary part denoted by a `j`. | `z = 2 + 3j` |

You can use the built-in `type()` function to verify the data type of any variable:

```py
# --- Integers (int) ---
positive_int = 105
negative_int = -23
large_int = 1_000_000  # You can use underscores for readability

print(type(positive_int))  # Output: <class 'int'>

# --- Floating-point numbers (float) ---
simple_float = 3.14
negative_float = -0.005
scientific_float = 2.5e3  # Equivalent to 2500.0 (2.5 * 10^3)

print(type(simple_float))  # Output: <class 'float'>

# --- Complex Numbers (complex) ---
complex_num = 4 + 5j
pure_imaginary = 2j

print(type(complex_num))  # Output: <class 'complex'>
print(complex_num.real)  # Output: 4.0
print(complex_num.imag)  # Output: 5.0
```

You can convert from one number type to another using the `int()`, `float()`, and `complex()` constructor functions:

```py
# Convert int to float
a = float(5)  # Result: 5.0
# Convert float to int (this rounds down toward zero)
b = int(9.99)  # Result: 9
# Convert int to complex
c = complex(3)  # Result: (3+0j)
```

__The size of `int`/`float`/`complex`__ is fixed. Unlike in Python, `int` doesn't expand to fit any arbitrary size. 

```py
import sys

print(sys.getsizeof(0))          # Output: 4 bytes
print(sys.getsizeof(1))          # Output: 4 bytes
print(sys.getsizeof(3.14))       # Output: 8 bytes
print(sys.getsizeof(1+2j))       # Output: 16 bytes (2 floats)
```

To use Python's native number objects, import them from the `python` module. Number literals will use those types instead of Pylem's numbers.

```py
from python import int, float, complex
import sys

print(sys.getsizeof(0))          # Output: 28 bytes
print(sys.getsizeof(1))          # Output: 28 bytes
print(sys.getsizeof(3.14))       # Output: 28 bytes
print(sys.getsizeof(1+2j))       # Output: 28 bytes
print(sys.getsizeof(2**30))      # Output: 32 bytes (Grows as value expands)
print(sys.getsizeof(2**1000))    # Output: 168 bytes
```

##### Sized Number Types

In addition to Python's number types, Pylem includes size specific variants of integers (signed or unsigned) and floating-point numbers to give you more control.

| Category | Available Types | Description |
|:---|:---|:---|
| Signed Integers | `i8`, `i16`, `i32`, `i64`, `i128`, `isize` | Can be positive or negative |
| Unsigned Integers | `u8`, `u16`, `u32`, `u64`, `u128`, `usize` | Only positive values or zero |
| Floating-Point | `f32`, `f64` | Numbers with decimal parts |

The `isize` and `usize` types depend entirely on your computer's architecture (e.g., 64-bit on a 64-bit system) and are primarily used to index collections.

You can strictly declare your variable type using a colon (`:`).

```py
small_pos_number: u8 = 255        # 8-bit unsigned integer
negative_number: i16 = -32000     # 16-bit signed integer
high_precision: f32 = 2.71828     # 32-bit single-precision float
```

The type can be appended directly to the literal value as a suffix. You can also inject underscores `_` into long numbers to improve scannability without breaking your code.

```py
byte_value = 57u8                 # Explicitly a u8 literal
big_million = 1_000_000_i64       # Separated for clarity, type i64
float_suffix = 4.5f32             # Explicitly an f32 literal
```

You can represent integers using binary, octal, or hexadecimal notation via distinct prefixes. 

```py
hex_val = 0xff                    # Hexadecimal (Base 16) = 255
octal_val = 0o77                  # Octal (Base 8) = 63
binary_val = 0b1111_0000          # Binary (Base 2) = 240
```

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

A string is a sequence of characters enclosed in single (`'`), double (`"`), or triple quotes (`"""`).

You can use single or double quotes interchangeably to define a standard text string.

* Single quotes: `message = 'Hello, World!'`
* Double quotes: `name = "Pylem programming"`
* Quotes inside quotes: Use double quotes if you need a literal single quote inside, or vice versa.

```py
quote = "It's a beautiful day"  # No escaping needed
```

There's also a specialized string types for multiline layouts, formatting, or working with file paths.

* Multiline strings: Created using three single or double quotes, preserving line breaks.

```py
multiline = """
This is a string
that spans multiple
lines.
"""
```

* F-Strings (Formatted strings): Prefixed with `f` to embed variables directly inside the text.

```py
age = 25
status = f"I am {age} years old."
```

* Raw strings: Prefixed with `r` to treat backslashes as literal characters instead of escape characters (great for Windows file paths).

```py
path = r"C:\Users\Name\Documents"
```

Strings are immutable, meaning you cannot change them in place, but you can build new ones through operations.

* Concatenation: Combining strings using the `+` operator.

```py
full_name = "Guido" + " " + "van Rossum"
```

* Slicing: Extracting specific parts of a string using index brackets [start:end].

```py
word = "Anaconda"
print(word[0:3])  # Outputs: Ana
```

_[Built-in Types](#built-in-types)_

#### Arrays (`arr` / `list`)

Array types are split between the familiar and dynamic lists from Python `list[T]` and the more low-level, static C-style arrays `arr[T, N]`. *(Skip to [`arr`](#arr) if you want to see the type unique to Pylem.)*

By default, arrays in Pylem are static `arr` type. To make a dynamic array, you must eplicitly declare a `list` type.

##### `list`

Lists are created by placing items inside square brackets `[]` in a context where a `list` is expected, separated by commas. This is similar to how `chr` characters are differentiated from `str` strings. You can either declare a type as `list` or cast an array with the `list()` constructor.

```py
fruits: list[str] = ["apple", "banana", "cherry"]
prices = list[float]([1.99, 0.98, 1.45])
numbers = list([10, 20, 30, 40])
```

* Empty List: An initialized list with no elements inside yet.

```py
empty_list: list = []
empty_list = list()
```

* Nested List (2D List): A list that contains other lists inside it, often used for grids or tables.

```py
matrix: list[list[int]] = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
```

* List of Dictionaries: Frequently used to store structured data or API responses.

```py
users: list[dict[str, str]] = [
    {"name": "Bob", "age": "30"},
    {"name": "Charlie", "age": "25"}
]
```

There are several built-in methods to change list content dynamically like in Python:

```py
# Start with a list
inventory = ["laptop", "mouse"]
# Add an item to the end
inventory.append("keyboard")  # ['laptop', 'mouse', 'keyboard']
# Insert an item at a specific index
inventory.insert(1, "monitor")  # ['laptop', 'monitor', 'mouse', 'keyboard']
# Remove an item by its name
inventory.remove("mouse")  # ['laptop', 'monitor', 'keyboard']
# Remove and return the last itemlast_item = inventory.pop()  # 'keyboard' (inventory is now ['laptop', 'monitor'])
```

Items are accessed using zero-based indexing (the first item is 0). Indexing a `list` out of bounds will still throw an `IndexError` like in Python, 

```py
colors: list = ["red", "green", "blue"]

print(colors[0])   # Outputs: red
print(colors[-1])  # Outputs: blue (negative indexing counts from the back)
print(colors[3])   # IndexError
print(colors[-4])  # IndexError
```

##### `arr`

Static arrays don't have as many bells and whistles as lists. They're designed to be a low-level data type for where performance is critical.

Static arrays are declared like lists but in contexts where an `arr` type is expected, similar to `chr`. You can also use the constructor `arr()` on an array literal which will compile to a static array with no overhead or casting. By default, an array literal `[]` will be compiled as a static array if there is no context.

```py
chr_arr: arr[chr, 5] = ['h',"e",'l',"l",'o']
int_arr = arr[int, 4]([1, 2, 3, 4])
float_arr = arr([5.0, 5.1, 5.2])
unallocated_arr = arr[int, 5]()
int_arr = [1, 2, 3, 4]    # `arr` by default
```

Casting between an array and a list is also possible, although it'll come with overhead cost at run-time. If the list is smaller than the array, then the rest will be allocated with the type's default value.

```py
l: list[int] = [1, 2, 3, 4, 5]
a: arr[int, 5] = arr(l)
```

Items are accessed using zero-based indexing (the first item is `0`). Indexing an `arr` out of bounds can cause a crash, although the error can't be caught since it's doing a raw deference on a pointer like in C. Every `arr` is also a `ptr` type. If you have `a: arr`, then `a[1]` is the same as `(a + 1).*`. Because of that, negative array indexing doesn't work since that would require checking for positive or negative which adds run-time overhead on the dereference operation. 

```py
colors = ["red", "green", "blue"]

mut item: str

item = colors[0]
print(item)   # Outputs: red

# item = colors[-1]           # Out of bounds crash
item = colors[len(colors)-1]  # Do this instead
print(item)   # Outputs: blue
```

To keep the operation fast and lightweight, you must only index with positive integers between `0` and `len(a)-1`. Note that `len(a)` on a fixed size array is a constant expression with no run-time overhead.

_[Built-in Types](#built-in-types)_

#### Dictionaries (`dict`)

A dictionary `dict[T, U]` is a built-in data structure used to store data in `key:value` pairs, where each unique key maps to a specific value. You can define a dictionary by placing your `key:value` pairs inside curly braces `{}` and separating them with commas.

```py
# A dictionary representing user profile data
user_profile: dict[str, str] = {
    "username": "coder123",
    "email": "coder123@example.com",
    "login_count": "5",
    "is_active": "True"
}

print(user_profile)
# Output: {'username': 'coder123', 'email': 'coder123@example.com', 'login_count': '5', 'is_active': 'True'}
```

You can look up a value by passing its matching key inside square brackets `[]`, or by safely using the `.get()` method to avoid errors if the key does not exist.

```py
# 1. Standard square bracket look-up
print(user_profile["username"])  # Output: coder123
# 2. Safe look-up using .get()
print(user_profile.get("is_active"))  # Output: True
# Using .get() with a fallback default value for missing keys
print(user_profile.get("theme", "Dark Mode"))  # Output: Dark Mode
```

Dictionaries are mutable when declared with `mut`, meaning you can update existing values or add completely new pairs on the fly.

```py
mut user_profile = {
    "username": "coder123",
    "email": "coder123@example.com",
    "login_count": "5",
    "is_active": "True"
}

# Updating an existing value
user_profile["login_count"] = "6"
# Adding a brand new key-value pair
user_profile["country"] = "Canada"

print(user_profile)
# Output: {'username': 'coder123', 'email': 'coder123@example.com', 'login_count': '6', 'is_active': 'True', 'country': 'Canada'}
```

You can remove specific items on mutable dictionaries using the `del` keyword or the `.pop()` method (which also returns the removed value).

```py
# Using del to remove an itemdel user_profile["is_active"]
# Using .pop() to remove an item and save its value
removed_email = user_profile.pop("email")

print(user_profile)
# Output: {'username': 'coder123', 'login_count': '6', 'country': 'Canada'}
```

You can loop through just the keys, just the values, or both simultaneously using `.items()`.

```py
inventory: dict[str, int] = {"apples": 10, "bananas": 4, "oranges": 7}
# Looping through keys and values together
for fruit, quantity in inventory.items():
    print(f"We have {quantity} {fruit}.")
# Output:
# We have 10 apples.
# We have 4 bananas.
# We have 7 oranges.
```

_[Built-in Types](#built-in-types)_

#### Tuples

A tuple is an ordered collection of items written with parentheses `()`. You can store multiple data types together, or even create a tuple with just a single item (which requires a trailing comma).

```py
# A standard tuple of strings
fruits = ("apple", "banana", "cherry")
# A mixed data type tuple (integer, string, float, boolean)
mixed_tuple = (10, "Pylem", 3.14, True)
# A single-item tuple (requires a trailing comma)
single_item = ("solo",)
```

Tuples are indexed starting at `[0]`. You can extract specific items or sections using slicing:

```py
coordinates = (4, 10, 18)

print(coordinates[0])   # Output: 4
print(coordinates[-1])  # Output: 18 (gets the last item)
print(coordinates[0:2]) # Output: (4, 10)
```

Tuples are immutable by default like they are in Python. However, they can be made mutable with `mut`, but their length can't change. They're like a `struct` but accessed with array indexing `[0]`. The number passed to the square brackets must be known at compile time, such as a constant or number literal.

```py
colors = ("red", "green", "blue")
# Trying to change an item will throw an error
colors[0] = "yellow" # TypeError: 'tuple' object does not support item assignment
```

```py
mut colors = ("red", "green", "blue")
colors[0] = "yellow" # OK
```

Because immutable tuples cannot be altered, developers use them for data that must remain constant throughout a program.

* Fixed Coordinates / Points: Keeping X and Y values locked together.

```py
location = (40.7128, -74.0060) # Latitude and Longitude
```

* Returning Multiple Values from Functions:

```py
def get_user():
    return ("Alice", 25) # Returns a tuple
name, age = get_user() # Unpacks the tuple into variables
```

* Dictionary Keys: Unlike lists, tuples can be used as keys in a dictionary because they are hashable.

```py
connections = {("New York", "London"): 5500}
```

_[Built-in Types](#built-in-types)_

#### None-ables (`?`)

In Python, it's common to set things to `None` if you haven't set it yet. This works in dynamically typed languages, but Pylem is statically typed. To make this work, some values can be set to `None` if its type is declared with a question mark `T?`. This must be checked for `None` before using.

```py
x: int? = get_number()

if x is not None:
    # x is safe here
    print(f"The number is {x}")
else:
    print("No number")
```

Internally, what's happening is that the value becomes a tagged union with 2 variants: *`Some` value* or `None`. *(See [`enum union`](#enum-union).)* When you enter a block where it's guaranteed not to be `None`, then it's automatically unwrapped inside that block.

A simplified version of what it's doing under the hood might look something like this:

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

When you use a type `T?` where a type `T` is expected, it will be unwrapped automatically which can raise a `TypeError` exception. This mimics trying to use `None` in Python on something that doesn't accept `None`. You can also use the `unwrap()` function to force a `T?` type to unwrap, raising an `UnwrapError` if it doesn't.

```py
try:
    i: int = unwrap(get_number())  # Might raise if None.
    print(f"Result: {i}")
except UnwrapError as e:
    print(f"Error: {e}")
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

#### Pointers (`ptr`)

Pointers are type `ptr[T]`. You can get the reference to something with the function `ref`. The postfix `.*` operator will dereference a pointer. A `mut` pointer must point to a reference also declared with `mut`.

```py
mut x = 0
mut xPtr: ptr[int] = ref(x)
xPtr.* = 1
x  # Value: 1
```

Safety pointers use a None-able type `ptr?`. If a pointer can't be guaranteed to not be NULL, then it must use a safety pointer type. Checking for `None` before dereferencing will coerce it to a raw pointer that can be dereferenced safely. Otherwise, dereferencing it might raise an error at run-time.

```py
def check_ptr(p: ptr[int]?):
    if p is not None:
        n: int = p.*  # Safe to derefence
        print(f"p.* is {n}")

i = 1
check_ptr(ref(i))
# Print: "p.* is 1"
```

Note that a safety pointer `ptr[T]?` is related to but not quite the same as a `ptr[T?]` or in other words *a non-null pointer to a value that might be `None`.* A `ptr[T?]` can be safely dereferenced at any time, but its value is still wrapped in a `T?` that needs to be checked for `None`. However, you can dereference it to check for `None` and it will also coerse to a `ptr[T]` type just like a safety pointer.

```py
x: int? = get_number()
p: ptr[int?] = ref(x)           # Non-null pointer to an optional int

if p.* is not None:             # Check the value instead of the pointer
    print(f"p.* is {p.*}")      # p.* will automatically unwrap to an int here.
```

_[Built-in Types](#built-in-types)_

#### Dynamic Type (`dyn`)

Pylem is statically typed, but Python is famous for being dynamically typed. Sometimes, it's hard to go from dynamic to static. To help with that, Pylem comes with a special type to handle dynamically typed data.

The dynamic type `dyn` is an API to access Python's dynamic typing from within Pylem. This works as a tagged union where each tag is a basic type: `Bool`, `Int`, `Float`, `Complex`, `Str`, `List`, `Dict`, `Tuple`, and `None`. Each of these are variants of `dyn` like `dyn.Bool`, `dyn.None`, etc. If the type has a subtype, then it's also set to `dyn`. 

```py
def print_dyn(d: dyn, prefix=""):
    match d:
        case Bool as b if b:
            print(f"{prefix}bool: True")
        case Bool as b if not b:
            print(f"{prefix}bool: False")
        case Int as i:
            print(f"{prefix}int: {i}")
        case Float as f:
            print(f"{prefix}float: {f}")
        case Complex as c:
            print(f"{prefix}complex: {c}")
        case Str as s:
            print(f"{prefix}str: {s}")
        case List as l:
            print(f"{prefix}list:")
            next_prefix = "* " if len(prefix) == 0 else "  " + prefix
            for item in l:
                print_dyn(item, next_prefix)
        case Dict as d:
            print(f"{prefix}dict:")
            next_prefix = "* " if len(prefix) == 0 else "  " + prefix
            key_prefix = next_prefix + "(key) "
            val_prefix = next_prefix + "(val) "
            for key, val in d.items():
                print_dyn(key, key_prefix)
                print_dyn(val, val_prefix)
        case Tuple as t:
            print(f"{prefix}tuple:")
            next_prefix = "* " if len(prefix) == 0 else "  " + prefix
            for item in t:
                print_dyn(item, next_prefix)
        case None:
            print(f"{prefix}None")
```

Since `dyn` already has `None` as one of its variants, its question type is redundant. If you type something as `dyn?`, the question mark will just be dropped and ignored.

_[Built-in Types](#built-in-types)_

### Custom Types

1. __[`type`](#type)__ — *Aliases*
2. __[`struct`](#struct)__ — *Structured Data*
3. __[`enum`](#enum)__ — *Enumerated Data*
4. __[`union`](#union)__ — *Untagged Unions*
5. __[`enum union`](#enum-union)__ — *Tagged Unions*
6. __[`class`](#class)__ — *Virtual Interfaces*

_[Types](#types)_

#### `type`

Creates an alias to another type.

```py
# Creating a type alias
type Point2D = tuple[float, float]

# Using it in a function signature
def move_point(point: Point2D) -> Point2D:
    return (point[0] + 1.0, point[1] + 1.0)
```

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

```py
# Define the enum
enum TrafficLight:
    Red
    Yellow
    Green

# Instantiate a variant using the period (.) syntax
current_light = TrafficLight.Green
# Read the value using a match expression
match current_light:
    case Red:    print("Stop!")
    case Yellow: print("Slow down!")
    case Green:  print("Go!")
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
    chr

u = SumUnion(int=1)

u.int    # Value is 1
u.float  # Read binary representation of int 1 as if it were a float
u.chr    # Read binary representation of int 1 as if it were a, value is '\1'
```

This is similar to C unions where it doesn't do any conversion; it only reads whatever data is there with a different type. Unions will set overflow data to 0 so that if you set a small member and then read from a big member, you won't get undefined behavior. The zero-padding interacts with endianness in a way that's deterministic but platform-dependent. The behavior is always defined, just not always portable. 

```py
u = SomeUnion(chr='\1')   # chr (1 byte), remaining bytes zeroed

# Little-endian: memory is [0x01, 0x00, 0x00, 0x00]
u.int          # Value: 1

# Big-endian: memory is [0x01, 0x00, 0x00, 0x00]  (same bytes)
u.int          # Value: 0x01000000 = 16777216
```

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

_[Custom Types](#custom-types)_

#### `enum union`

A union can be tagged with an anonymous enum by declaring it with `enum union`. This blends the concepts of enums and unions together to create a **true sum type** and will allow you to instantiate it with each member as a variant. Varients without data are empty and set to `void`.

```py
enum union MyTaggedUnion:
    First
    Second: int
    Third: {val: int}

a = MyTaggedUnion.First
b = MyTaggedUnion.Second(2)
c = MyTaggedUnion.Third(val=3)

match a:
    case First:
        print("first!")
    case Second as val:
        print(f"second! {val}")
    case Third as x:
        print(f"third! {x.val}")
```

```py
enum union WebEvent:
    PageLoad
    KeyPress: chr
    Paste: str
    Click: { x: i64, y: i64 }

# Create an instance of a variant with structured data
click_event = WebEvent.Click(x=40, y=120)

# Destructure data inside the match statement to read the payload
match click_event:
    case PageLoad:
        print("Page loaded successfully.")
    case KeyPress as c:
        print(f"Pressed key: {c}")
    case Paste as text:
        print(f"Pasted text: {text}")
    case Click as { x, y }:
        print(f"Clicked at coordinates x: {x}, y: {y}")
```

```py
enum union Command:
    # No data needed
    Undo
    # Struct-like: explicit, named fields
    MoveTo: { x: i32, y: i32 }
    # Tuple-like: single value
    Write: str
    # Tuple-like: anonymous color data (R, G, B)
    ChangeColor: u8, u8, u8

def execute(command: Command):
    match command:
        case Undo: print("Reverting last action.")
        case MoveTo as { x, y }: print(f"Moving cursor to ({x}, {y}).")
        case Write as text: print("Writing text to buffer: \"{text}\"")
        case ChangeColor as r, g, b: print(f"Color changed to RGB({r}, {g}, {b})")

action = Command.ChangeColor(255, 0, 128)
execute(action)
```

```py
# A custom struct used inside the enum variant payload
struct UserProfile:
    username: str
    avatar_url: str

enum union NetworkResponse:
    # App is waiting
    Idle
    # App is fetching data
    Loading
    # Payload is a custom data struct
    Success: UserProfile
    # Payload contains error details
    Failure: { code: u32, message: str }

def render_ui(response: NetworkResponse):
    match response:
        case Idle:
            print("Welcome! Click the button to load your profile.")
        case Loading:
            print("Fetching data from server... Please wait.")
        case Success as profile:
            print(f"Profile loaded! User: {profile.username}, Avatar: {profile.avatar_url}")
        case Failure as { code, message }:
            print(f"Error {code}: Data fetch failed. Reason: {message}")

current_state = NetworkResponse.Failure(
    code = 404, 
    message = "Not Found"
)
render_ui(current_state)
```

```py
enum FilePermission:
    ReadOnly
    ReadWrite

enum union Node:
    File: { 
        name: str, 
        size_kb: u64, 
        perms: FilePermission
    }
    Directory: { 
        name: str, 
        item_count: u32 
    }

def inspect_node(node: Node):
    match node:
        case File as { name, size_kb, perms }:
            print(f"File: {name} ({size_kb} KB) - Permission: ")
            match perms:
                case ReadOnly: print("Read Only")
                case ReadWrite: print("Read & Write")
        case Directory as { name, item_count }:
            print(f"Directory: {name} containing {item_count} items.")

my_file = Node.File(
    name = "config.toml",
    size_kb = 4,
    perms = FilePermission.ReadWrite
)
inspect_node(my_file)
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
    def deposit(mut self: ptr, amount: int):
        self.balance += amount
```

__Interfaces:__ an interface is a class without any data. It works like `interface` or `trait` in other languages.

```py
# Defines a contract (Works like Rust's `trait Renderable`)
class Renderable:
    def render(self: ptr) -> str:
        pass
```

Implement an interface into another class by extending it. Each `class` definition adds new methods to a type, much like how each `def` block of the same function overloads it.

```py
# Implement the 'Renderable' behavior specifically for 'BankAccount'
class BankAccount(Renderable):
    def render(self: ptr) -> str:
        return f"Account owner: {self.owner}, Balance: {self.balance}"
```

__Types of `self`:__ By itself, `self` copies the object into the method. You can also use a pointer to self instead. `ptr` are inferred to be of the same type as the class that's being defined.

- `self` – Immutable copy of the object.
- `mut self` – Mutable (within the function) copy of the object.
- `self: ptr` – Immutable reference of the object.
- `mut self: ptr` – Mutable reference of the object.

__Constructors:__ When a type has one or more `__init__(mut self: ptr)` methods defined, you can use that to create the type instead of the standard instantiation method. This can be overloaded to create multiple ways to initiate a type. The first argument `mut self: ptr` is an unset reference to the new object. If it's a struct, then all members need to be set. If it's an enum or union, then it must be set to one of its variants.

```py
class BankAccount:
    def __init__(mut self: ptr, owner, balance=0):
        self.owner = owner
        self.balance = balance

# Creating an object instance
my_account = BankAccount("Alex", 100)
print(f"{my_account.owner} has ${my_account.balance}")
```

#### Dunder Methods

__Dunder *(shourt for "double underscore")* Methods__ are special methods marked with 2 underscores (`__`) before and after the name of the method.

* `__init__(mut self: ptr, ...)`: Initializes a newly created instance of a class.
* `__new__(cls, ...)`: The true constructor that allocates memory for the new object, running right before __init__.
* `__del__(self)`: The destructor method triggered when an object is about to be garbage collected.
* `__str__(self)`: Defines user-friendly, readable text for `str()`.
* `__repr__(self)`: Returns an explicit, unambiguous string meant for debugging and logging.
* `__enter__(self)`/`__exit__(self, ...)`: Define the behavior of the object when used in a [`with`](#with) block.
* `__add__(self, other)` etc.: *See [Operator Overloading](#operator-overloading).*
* `__iter__()`/`__next__()`: *See [Iterators & Asynchronous Functions](#iterators--asynchronous-functions).*
* `__aiter__()`/`__anext__()`: *See [Asynchronous Iterators](#asynchronous-iterators).*

_[Custom Types](#custom-types)_

[TOC](#table-of-contents)

---

## Operators

### Unique Operators

Pylem includes some new operators that are not found in Python.

| Operator | Description | Precedence | Associativity |
|:---|:---|---:|:---|
| `x?[index]`, `x?[index:index]`, `x?(arguments...)`, `x?.attribute` | Safe subscription (indexing), slicing, function call, and attribute reference to a question type `T?`; wraps in a type `T?`; returns `None` if `x` is `None` | 2 | Left-to-right |
| `x.*` | Dereference a pointer | 2 | Left-to-right |
| `x?.*` | Dereference a nullable pointer: for a pointer type `ptr[T]?`, returns type `T?` | 2 | Left-to-right |
| `??` | `None`-coalessing / fallback operator | 17 | Left-to-right |

When accessing something from a pointer type `ptr`, dereferencing with `.*` isn't necessary. Assuming `p` is a pointer, then:

- `p.member` → `p.*.member`
- `p[index]` → `p.*[index]`
- `p[index:index]` → `p.*[index:index]`
- `p(arguments...)` → `p.*(arguments...)`

Or if `p` is a nullable pointer type `ptr?`, then:

- `p?.member` → `p?.*?.member`
- `p?[index]` → `p?.*?[index]`
- `p?[index:index]` → `p?.*?[index:index]`
- `p?(arguments...)` → `p?.*?(arguments...)`

Even if you have nested pointers, these operators will automatically dereference each one — for example, if `p` is `ptr[ptr[T]]`, then `p.member` will mean `p.*.*.member`, etc..

`.await` follows standard member access rules and composes with `?.` and `.*` accordingly. *See [Iterators & Asynchronous Functions](#iterators--asynchronous-functions).*

### Overlapping Operators

The same operators in Python are also in Pylem.

| Precedence | Operator | Description | Associativity |
|---:|:---|:---|:---|
| (Highest) __1__ | `(Expressions...)`, `[Expressions...]`, `{Key: Value...}`, `{Expressions...}` | Binding or parenthesized expression, list display, dictionary display, set display | Left-to-right |
| __2__ | `x[index]`, `x[index:index]`, `x(arguments...)`, `x.attribute` | Subscription (indexing), slicing, function call, attribute reference | Left-to-right |
| __3__ | `await x` | Await expression | N/A |
| __4__ | `**` | Exponentiation (power) | Right-to-left |
| __5__ | `+x`, `-x`, `~x` | Unary positive, unary negative, bitwise NOT | Right-to-left |
| __6__ | `*`, `@`, `/`, `//`, `%` | Multiplication, matrix multiplication, division, floor division, remainder/modulo | Left-to-right |
| __7__ | `+`, `-` | Addition and subtraction | Left-to-right |
| __8__ | `<<`, `>>` | Bitwise left and right shifts | Left-to-right |
| __9__ | `&` | Bitwise AND | Left-to-right |
| __10__ | `^` | Bitwise XOR | Left-to-right |
| __11__ | `\|` | Bitwise OR | Left-to-right |
| __12__ | `in`, `not in`, `is`, `is not`, `<`, `<=`, `>`, `>=`, `!=`, `==` | Comparisons, including membership tests and identity tests | Left-to-right (Chained) |
| __13__ | `not x` | Boolean / Logical NOT | Left-to-right |
| __14__ | `and` | Boolean / Logical AND | Left-to-right |
| __15__ | `or` | Boolean / Logical OR | Left-to-right |
| __16__ | `if` – `else` | Conditional expression (Ternary operator) | Right-to-left |
| __17__ | `lambda` | Lambda expression | N/A |
| (Lowest) __18__ | `:=` | Assignment expression (Walrus operator) | Right-to-left |

You can chain any comparison operator together, including relational, equality, identity, and membership operators:

* Relational: `<`, `>`, `<=`, `>=`
* Equality: `==`, `!=`
* Identity: `is`, `is not`
* Membership: `in`, `not in`

```py
# 1. Standard Range Check
age = 25
if 18 <= age < 65:
    print("Eligible for standard adult ticket")
# 2. Chained Equality Check
x = y = z = 100
if x == y == z:
    print("All three variables are exactly equal")
# 3. Mixing Different Operators (Arbitrary Chaining)
score = 85
if 0 < score <= 100 != 50:
    print("Valid score and it is not a tie benchmark")
```

Adjacent elements are evaluated individually. Writing `a > b < c` translates strictly to `(a > b) and (b < c)`. It does not imply or verify any mathematical relationship between `a` and `c`.

Because `is` and `in` are technically comparison operators, chaining them with equality can produce highly unexpected bugs.

```py
# ❌ INCORRECT LOGIC
status = [True, False]
if True in status == True:
    print("This will NOT print!")

# Why? Python translates it to: (True in status) and (status == True)
# "True in status" evaluates to True.
# "status == True" evaluates to False (a list is not a boolean).
# True and False results in False.

#  CORRECT LOGIC
if (True in status) == True:
    print("This prints as expected")
```

#### Compound Assignment Operators

| Operator | Name | Example | Equivalent To |
|:---:|:---|:---|:---|
| `+=` | Addition assignment | `x += 3` | `x := x + 3` |
| `-=` | Subtraction assignment | `x -= 3` | `x := x - 3` |
| `*=` | Multiplication assignment | `x *= 3` | `x := x * 3` |
| `/=` | Division assignment | `x /= 3` | `x := x / 3` |
| `//=` | Floor division assignment | `x //= 3` | `x := x // 3` |
| `%=` | Modulus assignment | `x %= 3` | `x := x % 3` |
| `**=` | Exponentiation assignment | `x **= 3` | `x := x ** 3` |
| `&=` | Bitwise AND assignment | `x &= 3` | `x := x & 3` |
| `\|=` | Bitwise OR assignment | `x \|= 3` | `x := x \| 3` |
| `^=` | Bitwise XOR assignment | `x ^= 3` | `x := x ^ 3` |
| `>>=` | Bitwise right shift assignment | `x >>= 3` | `x := x >> 3` |
| `<<=` | Bitwise left shift assignment | `x <<= 3` | `x := x << 3` |
| `:=` | Walrus operator (Assignment expression) | `if (n := len(a)) > 10:` | *Assigns and returns value* |

#### Operator Overloading

Operator overloading is defined using __[dunder methods](#dunder-methods).__

__Comparison Operators:__ *These methods handle equality and inequality operations. They typically return `True` or `False`.*

* `__lt__(self, other)`: Less than (`<`)
* `__le__(self, other)`: Less than or equal to (`<=`)
* `__eq__(self, other)`: Equal to (`==`)
* `__ne__(self, other)`: Not equal to (`!=`)
* `__gt__(self, other)`: Greater than (`>`)
* `__ge__(self, other)`: Greater than or equal to (`>=`)

__Arithmetic Operators:__ *These methods alter standard mathematical calculations.*

* `__add__(self, other)`: Addition (`+`)
* `__sub__(self, other)`: Subtraction (`-`)
* `__mul__(self, other)`: Multiplication (`*`)
* `__matmul__(self, other)`: Matrix multiplication (`@`)
* `__truediv__(self, other)`: True division (`/`)
* `__floordiv__(self, other)`: Floor division (`//`)
* `__mod__(self, other)`: Modulo/Remainder (`%`)
* `__divmod__(self, other)`: Combined division and modulo (`divmod()`)
* `__pow__(self, other[, modulo])`: Exponentiation (`**`)

__Reflected (Right-Hand) Arithmetic Operators:__ *Fallback to right-hand variants if the left operand does not support the corresponding operation.*

* `__radd__(self, other)`: Right addition (`+`)
* `__rsub__(self, other)`: Right subtraction (`-`)
* `__rmul__(self, other)`: Right multiplication (`*`)
* `__rmatmul__(self, other)`: Right matrix multiplication (`@`)
* `__rtruediv__(self, other)`: Right true division (`/`)
* `__rfloordiv__(self, other)`: Right floor division (`//`)
* `__rmod__(self, other)`: Right modulo (`%`)
* `__rdivmod__(self, other)`: Right division and modulo (`divmod()`)
* `__rpow__(self, other)`: Right exponentiation (`**`)

__In-Place (Assignment) Operators:__ *These methods govern compound assignment symbols like `+=` and `*=`.*

* `__iadd__(mut self: ptr, other)`: In-place addition (`+=`)
* `__isub__(mut self: ptr, other)`: In-place subtraction (`-=`)
* `__imul__(mut self: ptr, other)`: In-place multiplication (`*=`)
* `__imatmul__(mut self: ptr, other)`: In-place matrix multiplication (`@=`)
* `__itruediv__(mut self: ptr, other)`: In-place true division (`/=`)
* `__ifloordiv__(mut self: ptr, other)`: In-place floor division (`//=`)
* `__imod__(mut self: ptr, other)`: In-place modulo (`%=`)
* `__ipow__(mut self: ptr, other)`: In-place exponentiation (`**=`)

__Bitwise Operators:__ *These handle binary bit manipulation and logical bit masking operations.*

* `__lshift__(self, other)`: Bitwise left shift (`<<`)
* `__rshift__(self, other)`: Bitwise right shift (`>>`)
* `__and__(self, other)`: Bitwise AND (`&`)
* `__xor__(self, other)`: Bitwise XOR (`^`)
* `__or__(self, other)`: Bitwise OR (`|`)

__Reflected Bitwise:__

* `__rlshift__(self, other)`: Right bitwise left shift (`<<`)
* `__rrshift__(self, other)`: Right bitwise right shift (`>>`)
* `__rand__(self, other)`: Right bitwise AND (`&`)
* `__rxor__(self, other)`: Right bitwise XOR (`^`)
* `__ror__(self, other)`: Right bitwise OR (`|`)

__In-Place Bitwise:__

* `__ilshift__(mut self: ptr, other)`: In-place left shift (`<<=`)
* `__irshift__(mut self: ptr, other)`: In-place right shift (`>>=`)
* `__iand__(mut self: ptr, other)`: In-place AND (`&=`)
* `__ixor__(mut self: ptr, other)`: In-place XOR (`^=`)
* `__ior__(mut self: ptr, other)`: In-place OR (`|=`)

__Unary Operators:__ *These operators process only one single object operand.*

* `__neg__(self)`: Unary negation (`-obj`)
* `__pos__(self)`: Unary plus (`+obj`)
* `__abs__(self)`: Absolute value (`abs(obj)`)
* `__invert__(self)`: Bitwise inversion (`~obj`)

__Container Operators:__ *These overload syntax patterns natively used with dictionaries, lists, sets, and tuples.*

* `__len__(self)`: Returns collection size (`len(obj)`)
* `__getitem__(self, key)`: Indexing and slicing access (`obj[key]`)
* `__setitem__(self, key, value)`: Indexing assignment (`obj[key] = value`)
* `__delitem__(self, key)`: Deleting items (`del obj[key]`)
* `__contains__(self, item)`: Membership testing (`item in obj`)

_[Operators](#operators)_

[TOC](#table-of-contents)

---

## Advanced

1. __[Slices](#slices)__
2. __[Generics](#generics)__
3. __[Compile-time Functions](#compile-time-functions)__
4. __[Named Return Values](#named-return-values)__
5. __[Parameters](#parameters)__
6. __[Iterators & Asynchronous Functions](#iterators--asynchronous-functions)__
7. __[Decorators](#decorators)__
8. __[Memory Allocation](#memory-allocation)__
9. __[Importing & Modules](#importing--modules)__

[TOC](#table-of-contents)

---

### Slices

A slice is a reference to part of a sequenced type such as arrays, lists, and tuples. Slicing an array in Pylem works differently than slicing a list in Python. 

#### Slicing Lists

```py
numbers: list = [0, 10, 20, 30, 40, 50]

# 1. Standard slice (indices 1, 2, 3)
print(str(numbers[1:4]))    # Output: [10, 20, 30]

# 2. Omit start (defaults to 0)
print(str(numbers[:3]))     # Output: [0, 10, 20]

# 3. Omit stop (goes to the end)
print(str(numbers[3:]))     # Output: [30, 40, 50]

# 4. Copy the entire list
print(str(numbers[:]))      # Output: [0, 10, 20, 30, 40, 50]
```

You can count backward from the end of the sequence using negative numbers. `-1` represents the last item, `-2` the second to last, and so on.

```py
letters: list[chr] = ['a', 'b', 'c', 'd', 'e']

# Slice the last two elements
print(str(letters[-2:]))    # Output: ['d', 'e']

# Slice from index 1 up to (but excluding) the last element
print(str(letters[1:-1]))   # Output: ['b', 'c', 'd']
```

The step argument controls how Python skips through the sequence.

```py
numbers: list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Get every second element
print(str(numbers[::2]))    # Output: [0, 2, 4, 6, 8]

# Reverse a sequence (negative step)
print(str(numbers[::-1]))   # Output: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
```

Unlike standard indexing with a list (e.g., `numbers[100]`), which throws an `IndexError`, slicing handles out-of-bounds indices gracefully by capping them at the start or end of the sequence.

```py
my_list: list = [1, 2, 3]
print(str(my_list[1:100]))  # Output: [2, 3] (No crash!)
```

For lists, `a[:]` creates a new list object containing references to the original items. Modifying the list structure of the copy won't affect the original list. However, if the items inside are mutable objects (like nested lists), changes to those objects will reflect in both.

#### Slicing Arrays

By default, Python slices implicitly allocate memory and copy data. In a compiled language, this behavior introduces unacceptable hidden performance costs.

* Python: Slicing a list (my_list[1:4]) creates a brand-new list object and copies references to those items.
* Pylem: Slicing must return a view or a borrowed reference to the existing memory, It should be a two-word fat pointer (a data pointer and a length).

If a developer wants a copy in Pylem, they must explicitly ask for it to prevent hidden allocations.

```py
# --- Python Behavior ---
nums = [1, 2, 3, 4]
sub = nums[1:3]    # Allocates a new list [2, 3]
sub[0] = 99        # Modifies 'sub', 'nums' remains [1, 2, 3, 4]

# --- Pylem Behavior ---
nums = [1, 2, 3, 4]
sub = nums[1:3]     # ZERO allocation. 'sub' is a fat pointer pointing into 'nums'.
sub[0] = 99         # 'nums' becomes [1, 99, 3, 4] because it's a view!

# Explicit copying required for old Python behavior:
sub_copy = nums[1:3].copy() 
```

Slices must be strongly typed at compile time. Pylem needs to distinguish between an owned collection (like a Vector or Array) and a borrowed slice view.

```py
# Pylem type signatures (Conceptual syntax matching Python type hints)
def calculate_sum(data: slice[int]) -> int:
    # 'data' does not own memory; it's a lightweight view accepting 
    # fixed arrays, dynamic lists, or other sub-slices of ints.
    return sum(data)
```

A standard fat pointer (ptr + len) requires elements to be strictly contiguous in memory. To remain zero-allocation, Pylem should disallow the step argument in standard slices. Alternatively, a non-contiguous slice would require a third word (a stride parameter), turning it into a 3-word fat pointer. To maximize optimization like C/Rust, Pylem should separate this into a distinct type: `StridedSlice[T]`.

Because Pylem compiles down to native machine code without a heavy runtime or garbage collector, it faces the "dangling pointer" problem. If the original list is freed, the slice view becomes invalid.

Pylem must implement one of two strategies:

   1. Rust Approach (Lifetimes): The compiler tracks the slice and throws a compile-time error if the original collection is dropped or modified while the slice view is active.
   2. C++ Approach (Trivially Unsafe): The compiler allows it, but it becomes undefined behavior if the developer mismanages memory. To fit a modern compiled language, option 1 is highly preferred.

If a developer slices a fixed-size array using literals known at compile time, Pylem can optimize the slice into a fixed-size stack array view rather than a dynamic slice.

```py
# Pylem can optimize this at compile time
fixed_array: arr[int, 10] = [0] * 10
sub_view: arr[int, 3] = fixed_array[2:5] # Size (3) is known to the compiler
```

This silent capping requires branching logic (`if`/`else` checks) at runtime, which slows down execution loops. Pylem should treat out-of-bounds slicing as a runtime panic or a compiler optimization boundary to achieve C-like speeds.

_[Advanced](#advanced)_

---

### Generics

Generics allow you to write reusable code (functions or classes) that can operate on multiple data types while keeping static type safety. 

Use brackets to declare a type variable placeholder (like `[T]`), then use `T` for arguments and return types.

```py
# The [T] syntax automatically creates a type variable
def get_first_element[T](items: list[T]) -> T:
    return items[0]
# Type checkers automatically infer the type based on the input
number = get_first_element([1, 2, 3])      # Inferred as int
text = get_first_element(["a", "b", "c"])  # Inferred as str
```

You can create flexible data structures like a Box or Stack that can hold any type.

```py
struct Box[T]:
    content: T

class Box[T]:
    def __init__(mut self: ptr, content: T):
        self.content: T = content
    def get_content(self: ptr) -> T:
        return self.content
# Instantiate with specific types
int_box = Box[int](123)
str_box = Box[str]("Hello")
```

If you want a generic function to only accept specific types, you can pass them directly inside the bracket declaration.

```py
# T can only be an int or a float
def add_numbers[type T: (int, float)](a: T, b: T) -> T:
    return a + b
```

In addition to types, generics can also be constants. Overloaded functions and classes will use the same constraints, so you only need to declare them once.

```py
struct Array[type T, const N: usize]:
    data: arr[T, N]

class Array[T, N]:   # `type`/`const` constraint inherited from struct declaration
    def __init__(mut self: ptr, data: arr[T, N]):
        self.data = data

a = Array([1, 2, 3])  # Array[int, 3] inferred
```

`type` before a generic parameter is only needed when you're setting constraints or giving it a default value to distinguish it from a `const` parameter. Each can be inferred based on usage inside the generic function or type.

_[Advanced](#advanced)_

---

### Compile-time Functions

A `const` function is evaluated at compile time if its arguments are constant expressions. If the arguments are determined at runtime, the same function seamlessly executes as a normal runtime function.

This example calculates a value at compile time. The compiler completely eliminates the runtime math and replaces the function call with the literal value `120`.

```py
# Simple const function
const factorial(n: int) -> int:
    return 1 if n <= 1 else n * factorial(n - 1)

# Evaluated at compile time
const compile_time_val: int = factorial(5)

# Evaluated at runtime because the input depends on user interaction
i = int(input())
runtime_val = factorial(i) 

print(f"Compile-time: {compile_time_val}")
print(f"Runtime: {runtime_val}")
```

`const` functions are commonly used to compute parameters required by the compiler, such as the size of a raw array.

```py
const calculate_buffer_size(connections: int) -> int:
    return connections * 1024   # 1KB buffer per connection

# The compiler requires array dimensions to be known at compile time
mut raw_buffer: arr[int, calculate_buffer_size(5)]
print(f"Raw buffer size: {len(raw_buffer)} elements")
```

You can use variable declarations, loops, and conditional statements too.

```py
# Multi-statement
const sum_of_squares(n: int) -> int:
    sum = 0      # Local variables are allowed
    mut i = 1    # Can be mutable
    while i < n:
        sum += (i * i)
        i += 1
    return sum

const result: int = sum_of_squares(4)    # 1 + 4 + 9 + 16 = 30
print(f"Sum of squares: {result}")
```

__Const Structs and Methods:__ You can make constructors and member functions `const`. This lets you build and query complete objects entirely during the compilation phase.

```py
struct Point:
    x: float
    y: float

class Point:
    # Const constructor allows compile-time object initialization
    const __init__(mut self: ptr, start_x: float, start_y: float):
		self.x = start_x
		self.y = start_y

    # Const member function
    const get_manhattan_distance(self: ptr) -> float:
        return (-self.x if self.x < 0 else self.x) + (-self.y if self.y < 0 else self.y)

# The entire object is instantiated and evaluated by the compiler
const p = Point(3.5, -4.5)
const dist: float = p.get_manhattan_distance()

print(f"Manhattan Distance: {dist}")
```

__Summary of Rules for `const` Functions:__

* __No Side Effects:__ They cannot modify global state or call non-`const` functions.
* __Input-Driven Execution:__ If you pass a runtime variable as an argument, the function acts as a normal runtime function.
* __Literal Types:__ Arguments and return types must be literal types (such as `int`, `float`, pointers, or literal structs).
* __Enforced Evaluation:__ Simply marking a function `const` does not force the compiler to run it at compile time unless the output is assigned to a `const` variable or used in a template parameter.

_[Advanced](#advanced)_

---

### Named Return Values

Named Return Values allow you to declare variable names for your return types directly in the function signature. The return value can be set using a variable by declaring the return type with `as` after it. These are always mutable, so no `mut` is needed. If a function returns multiple return values, each can be declared with `as`. When you name your return values, you can use a **naked return** (a `return` statement without explicit arguments). The compiler automatically returns the current values of those variables.

```py
# sum and product are initialized to 0 automatically
def calculate(a: int, b: int) -> int as sum, int as product:
	sum = a + b
	product = a * b
	return # Naked return: automatically returns sum and product

s, p = calculate(3, 5)
print(f"Sum: {s}, Product: {p}") 
# Output: Sum: 8, Product: 15
```

```py
def get_coordinates() -> float as lat, float as lng:
	lat = 35.9606
	lng = -83.9207
	# You can still return explicitly if you prefer over naked returns
	return lat, lng 

latitude, longitude = get_coordinates()
print(f"Lat: {latitude}, Lng: {longitude}")
```

__Modifying Returns:__ A major specialized use case for named return values is interacting with `defer`. Because the named parameters are scoped to the entire function, a deferred closure can intercept and change the final values right before they reach the caller.

```py
def increment_score(base: int) -> int as final_score:
	# Evaluated last, right before the function exits
	defer:
        final_score += 5
	final_score = base + 10
	return # Sets finalScore to 15, then defer runs and adds 5

print(f"Final Score: {increment_score(5)}")
# Output: Final Score: 20
```

_[Advanced](#advanced)_

---

### Parameters

Pylem offers similar modifers to function parameters as Python.

#### Optional Parameters

Make a parameter optional by assigning it a default value in the function definition. If the caller provides a value for that parameter, it uses that; if they omit it, it falls back to the default. To create an optional parameter, use the assignment operator (`=`) followed by a fallback value. Required parameters must always come before optional ones.

```py
# 'name' is required, 'punctuation' is optional with a default value
def greet(name, punctuation="!"):
    return f"Hello, {name}{punctuation}"

# Call using only the required argument
print(greet("Alice"))        # Output: "Hello, Alice!"

# Call and overwrite the optional argument
print(greet("Bob", "?"))     # Output: "Hello, Bob?"
```

When a function has several optional parameters, you can use keyword arguments to target specific ones without worrying about their order.

```py
def make_coffee(size, milk="Whole", sugar=0, ice=False):
    mut summary = f"Size: {size}, Milk: {milk}, Sugar: {sugar} spoons"
    if ice:
        summary += ", Iced"
    return summary
# Uses all default values for the optional parameters
print(make_coffee("Medium"))             # Output: Size: "Medium, Milk: Whole, Sugar: 0 spoons"
# Targets only the 'ice' parameter using its keyword name
print(make_coffee("Large", ice=True))    # Output: Size: "Large, Milk: Whole, Sugar: 0 spoons, Iced"
```

If you do not want a literal default like `0` or `""`, use `None` as a placeholder. This will set it to a type `T?` when inferred. This allows you to check whether the caller passed a value.

```py
def create_profile(username, mut bio=None):
    if bio is None:
        bio = "No bio provided."
    return {"username": username, "bio": bio}

print(str(create_profile("coder123")))
# Output: "{'username': 'coder123', 'bio': 'No bio provided.'}"
```

Never use mutable objects (like lists or dictionaries) as default values. Default values only evaluated once when the function is defined, meaning all subsequent function calls share the exact same object.

```py
# ❌ INCORRECT: The list persists across calls
def add_to_list(item, my_list=[]):
    my_list.append(item)
    return my_list

print(add_to_list("apple"))  # Output: ['apple']
print(add_to_list("banana")) # Output: ['apple', 'banana'] (Bug: apple stayed!)
```

```py
# ✔️ CORRECT: Use None and instantiate the list inside the function
def add_to_list_correct(item, mut my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(item)
    return my_list

print(add_to_list_correct("apple"))  # Output: ['apple']
print(add_to_list_correct("banana")) # Output: ['banana'] (Fixed!)
```

#### Unlimited Optional Arguments (`*args` and `**kwargs`)
If you don't know how many optional arguments a user might pass ahead of time, you can accept a variable number of positional or keyword arguments.

* `*args`: Captures any extra positional arguments as a tuple.
* `**kwargs`: Captures any extra keyword arguments as a struct or dictionary.

```py
def print_package_details(*items, **metadata):
    print(f"Items in package: {items}")
    print(f"Shipping info: {metadata}")
# Pass any number of items and keyword-based metadata
print_package_details("Shoes", "Socks", "Shirt", carrier="FedEx", fragile=False)
# Output:
# "Items in package: ('Shoes', 'Socks', 'Shirt')"
# "Shipping info: {'carrier': 'FedEx', 'fragile': False}"
```

_[Advanced](#advanced)_

---

### Iterators & Asynchronous Functions

An **iterator** is an object that contains a countable number of values and implements the iterator protocol. This protocol consists of two special methods: `__iter__()` (which returns the iterator object itself) and `__next__()` (which returns the next item in the sequence). When no more elements are available, `__next__()` raises a `StopIteration` exception.

Collections like lists, tuples, and strings are iterables, meaning you can get an iterator from them using the built-in `iter()` function. You manually fetch items using `next()`.

```py
# Define an iterable list
fruits = ["apple", "banana", "cherry"]
# Get an iterator object from the list
fruit_iterator = iter(fruits)
# Fetch elements one by one
print(str(next(fruit_iterator)))  # Outputs: "apple"
print(str(next(fruit_iterator)))  # Outputs: "banana"
print(str(next(fruit_iterator)))  # Outputs: "cherry"
# Calling next() again will raise a StopIteration exception
# print(str(next(fruit_iterator)))
```

__Custom Class Iterators:__ You can build a custom iterator by creating a class that implements `__iter__()` and `__next__()`.

```py
class EvenNumbers:
    def __init__(mut self: ptr, max_limit):
        self.max_limit = max_limit
        self.current = 2

    def __iter__(self):
        return self

    def __next__(mut self: ptr):
        if self.current <= self.max_limit:
            value = self.current
            self.current += 2
            return value
        else:
            raise StopIteration

# Usage in a for-loop (which calls iter() and next() automatically)
evens = EvenNumbers(6)
for num in evens:
    print(str(num))  # Outputs: "2", "4", "6"
```

__Generator Iterators:__ Generators are the easiest way to create iterators. Any function that uses the `yield` keyword automatically returns a generator object, which conforms to the iterator protocol.

```py
def count_down(num):
    while num > 0:
        yield num
        num -= 1
# Instantiate the generator iterator
counter = count_down(3)

print(str(next(counter)))  # Outputs: "3"
print(str(next(counter)))  # Outputs: "2"
print(str(next(counter)))  # Outputs: "1"
```

__Memory-Efficient File Iterators:__ File objects are natively implemented as iterators. Instead of loading a massive file completely into your RAM, the file iterator yields one line at a time.

```py
# Memory-efficient line-by-line reading
with open("large_log.txt", "r") as file:
    for line in file:
        print(line.strip())
```

Like Python, Pylem provides highly optimized iterator tools via the built-in [itertools module](https://docs.python.org/3/library/itertools.html). They are perfect for memory-efficient data processing.

```py
import itertools
# Infinite loop iterator (safely capped here with a break)
for item in itertools.cycle(["A", "B", "C"]):
    print(item)  # Will print "A", "B", "C", "A", "B"... endlessly
    break        
```

Asynchronous programming in Pylem is primarily managed using the built-in [asyncio library](https://docs.python.org/3/library/asyncio.html) from Python. It relies on coroutines (defined with `async def`) and the `await` keyword to yield control back to an event loop while waiting for I/O operations to finish.

This entry-level example demonstrates how to declare an asynchronous function and run it inside the event loop using [`asyncio.run()`](https://docs.python.org/3/library/asyncio-task.html).

```py
import asyncio

# 1. Define an asynchronous function (coroutine)
async def main():
    print("Hello...")
    # 2. Pause execution non-blockingly for 1 second
    await asyncio.sleep(1)
    print("...World!")

# 3. Start the event loop and execute the coroutine
asyncio.run(main())
```

__Running Multiple Tasks Concurrently:__ To execute tasks simultaneously instead of waiting sequentially, group them into modern `asyncio.TaskGroup` context managers. This allows the event loop to juggle tasks during idle periods (like network or sleep delays).

```py
import asyncio
import time

async def fetch_data(id, delay):
    print(f"Task {id}: Fetching data...")
    await asyncio.sleep(delay)  # Simulates network lag
    print(f"Task {id}: Data received!")
	return f"Result {id}"

async def main():
    start_time = time.time()

    # TaskGroup manages scheduled operations together
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_data(1, 2))
        task2 = tg.create_task(fetch_data(2, 3))
        task3 = tg.create_task(fetch_data(3, 1))

    # The block implicitly awaits all tasks before exiting
    print(f"Results: {task1.result()}, {task2.result()}, {task3.result()}")
    print(f"Total time elapsed: {time.time() - start_time:.2f} seconds")

asyncio.run(main())
```

*Expected Output:*

```
Task 1: Fetching data...
Task 2: Fetching data...
Task 3: Fetching data...
Task 3: Data received!
Task 1: Data received!
Task 2: Data received!
Results: Result 1, Result 2, Result 3
Total time elapsed: 3.01 seconds (Takes the length of the longest task, not the sum of all tasks) [7] 
```

__Async Core Concepts Cheat Sheet:__

| Keyword / Tool | Purpose |
|---|---|
| `async def` | Declares a function as a coroutine wrapper rather than a normal synchronous function. |
| `await` | Pauses execution of the coroutine, giving control back to the loop until the event resolves. |
| `asyncio.run()` | The primary tool used to spin up an underlying event loop and drive a top-level coroutine. |
| `asyncio.gather()` | Waits for multiple asyncs to finish in parallel. |

Optionally, you can use `await` as a member on an async instance: `.await`. This works the same as the prefix operator version but has the same precedence as member access like `x.member`. It can be a useful alternative if you are going to chain a method on an async instance.

```py
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
	return "  Hello, Async World!  "

async def main():
    # Call the .strip() method directly on the awaited result
    result = fetch_data().await.strip()
    print(result)

asyncio.run(main())
```

In this example, `fetch_data().await.strip()` is the same as `(await fetch_data()).strip()`.

`.await` works like any member, so `?.await` and `.*.await` also work; however, use of those variants is rare since `async def` always returns an async instance, so you would need to wrap it in another function to need those other operators.

#### Iterator/Asynchronous Lambda Functions

As well as `def` functions, `lanbda` functions can also use `yield` and `await`. 

```py
# Utility function that consumes any generator function
def collect_values(generator_func, limit):
    iterator = generator_func()   # Initialize the anonymous generator
    mut results: list = []
    mut i = 0
    while i < limit:
        try:
            value = next(iterator)
            results.append(value)
            i += 1
        except StopIteration:
            break
    return results

# Passing an anonymous generator function inline
squares = collect_values(lambda:
    mut num = 1
    while True:
        yield num * num
        num += 1
, 5)

print(str(squares))
# Output: "[1, 4, 9, 16, 25]"
```

```py
# Utility function that processes chunks of data dynamically
def run_data_stream(stream_generator):
    stream = stream_generator()
	mut done = False
	while not done:
		try:
			value = next(stream)
            print(f"[Stream Processor] Received: {value}")
        except StopIteration:
            done = True
    print("[Stream Processor] Stream finished.")

# Passing an anonymous generator that acts as a mock server log stream
run_data_stream(lambda:
    yield "User logged in"
    yield "Updated profile picture"
    yield "Connected external bank account"
)

# Output:
# "[Stream Processor] Received: User logged in"
# "[Stream Processor] Received: Updated profile picture"
# "[Stream Processor] Received: Connected external bank account"
# "[Stream Processor] Stream finished."
```

Asynchronous lambda functions are declared using `async lambda`.

```py
import asyncio

# 1. Define a function that accepts an async function as a parameter
async def process_data(callback):
	print("Starting process...")
	# You must use await because callback() returns a Promise
	data = await callback()
	print(f"Processed user: {data["name"]}")

# 2. Pass the async function as an argument
asyncio.run(process_data(async lambda:
    await asyncio.sleep(1)
	return { "id": "1", "name": "Alice" }
))
```

```py
import asyncio

userIds = [1, 2, 3]

async def get_team_data() {
	# Passing the async function into map()
	promise_array = map(async lambda id:
	    await asyncio.sleep(1)
		f"User Profile {id}"
	, userIds)
	# promise_array is currently [Promise, Promise, Promise]
	results = await asyncio.gather(*promise_array)
	print(results)   # Output: "['User Profile 1', 'User Profile 2', 'User Profile 3']"

asyncio.run(get_team_data())
```

#### Asynchoronous Iterators

An asynchronous iterator is an object that implements the `__aiter__()` and `__anext__()` dunder methods, allowing you to stream data over time using the `async` for syntax.

There are two primary ways to create an asynchronous iterator: using a class-based custom protocol or using an asynchronous generator.

__Method 1: Class-Based Asynchronous Iterator__ This is the low-level method where you explicitly define the async iteration protocol. The `__anext__()` method must be a coroutine (defined with `async def`) and must `raise StopAsyncIteration` when the iteration is complete.

```py
import asyncio

class AsyncCounter:
    def __init__(mut self: ptr, stop_at):
        self.stop_at = stop_at
        self.current = 0
    def __aiter__(self):
        # Must return an object implementing __anext__
        return self
    async def __anext__(mut self: ptr):
        # Simulating an asynchronous I/O operation (like an API call)
        await asyncio.sleep(0.5) 
        if self.current >= self.stop_at:
            # Signals the end of the loop
            raise StopAsyncIteration
        self.current += 1
        return self.current

async def main():
    # Consume the class-based async iterator
    async for number in AsyncCounter(3):
        print(f"Counter item: {number}")

asyncio.run(main())
```

__Method 2: Asynchronous Generator (Recommended)__ Writing full iterator classes often introduces unnecessary boilerplate. An easier, more Pythonic approach is to write an asynchronous generator. Any async function using the yield keyword automatically implements the async iterator protocol under the hood.

```py
import asyncio

async def fetch_data_stream(limit):
    for i in range(1, limit + 1):
        # Simulating fetching a row or chunk from a database
        await asyncio.sleep(0.5) 
        yield f"Row {i} data"

async def main():
    # Consume the async generator iterator
    async for row in fetch_data_stream(3):
        print(f"Received: {row}")

asyncio.run(main())
```

_[Advanced](#advanced)_

---

### Decorators

A decorator is a function that takes another function as an argument, extends its behavior without modifying it explicitly, and returns a new function. You apply decorators by placing the `@decorator_name` syntax directly above your target function definition.

__Basic Decorator (No Arguments):__ This example prints a message before and after a function runs. It uses `functools.wraps` to preserve the original function's name and documentation.

```py
from functools import wraps

def my_logger(func):
    @wraps(func)
    def wrapper():
        print(f"--> Starting {func.__name__}")
        func()
        print(f"--> Finished {func.__name__}")
    return wrapper

@my_logger
def say_hello():
    print("Hello, World!")

say_hello()
```

*Output:*

```
--> Starting say_hello
Hello, World!
--> Finished say_hello
```

__Decorating Functions with Arguments:__ To decorate any function regardless of its inputs, use `*args` and `**kwargs` in the inner wrapper function to dynamically collect and pass arguments.

```py
import time
from functools import wraps
def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs) # Accepts any arguments
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result                  # Returns the actual function result
    return wrapper

@timer_decorator
def compute_power(base, exponent):
    return base ** exponent

print(str(compute_power(2, 100000)))
```

__Decorator Factories (Passing Arguments to the Decorator):__ If your decorator needs its own configuration parameters, you must add a third nesting level (a decorator factory) to handle the decorator's setup arguments.

```py
from functools import wraps
def repeat(num_times):
    def decorator_repeat(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat

@repeat(num_times=3)
def greet(name):
    print(f"Hello {name}")

greet("Alice") # Will print the greeting 3 times
```

_[Advanced](#advanced)_

---

### Memory Allocation

To allocate memory on the heap, use the `alloc` and `free` functions. The value passed to `alloc` will only run if it's able to allocate enough space. `alloc` returns a nullable pointer `ptr?`. Check for `None` to see if it succeeded or not. 

```py
struct Student:
    name: str
    grade: chr

mut student: ptr[Student]? = alloc(Student(name="John", grade='B'))
if student is not None:
	defer free(student)
	student.name = "John Smith"

def makeStudent(name: str, grade: chr) -> ptr[Student]?:
    return alloc(Student(name=name, grade=grade))
```

- `alloc` will check the size of the type passed to it and allocate that much space, returning a `ptr?`. If successful, it will run the expression in its parameter and return the pointer. If not, it will return `None`.
- `free` will free the memory to a pointer.

Instead of checking, you can force a pointer to not be null with `unwrap()`. This will raise an `UnwrapError` if it fails. 

```py
# Force a pointer to not be null with unwrap()
mut student: ptr[Student] = unwrap(alloc(Student(name="John", grade='B')))
defer free(student)
student.name = "John Smith"
```

_[Advanced](#advanced)_

---

### Importing & Modules

Importing pulls code from outside files, libraries, or modules into your current program so you can reuse it without rewriting it. When Pylem encounters an `import` statement, it searches for the specified file, runs its code, and creates an object representing that module in your current workspace. 

This approach imports the entire module. You must use a dot (`.`) prefix to access its internal variables, functions, or classes.

```py
import math
# Access the 'pi' variable inside the math module
print(math.pi)  # Output: 3.141592653589793
```

__Importing Specific Attributes:__ If you only need a specific function or variable, use the `from ... import ...` syntax. This lets you call the item directly without the module prefix.

```py
from random import randint
# Call the function directly
print(randint(1, 10))  # Output: A random number between 1 and 10
```

__Importing with an Alias:__ You can rename a module or function during the import using the `as` keyword. This is helpful for shortening long names or following industry conventions.

```py
import numpy as np
# Use the short 'np' alias instead of typing 'numpy'
my_array = np.array([1, 2, 3])
```

__Wildcard Import (Generally Discouraged):__ Using an asterisk `*` imports everything from a module into your local workspace.

```py
from math import *

print(sqrt(16))  # Output: 4.0
```

*⚠️ Why avoid this?* It pollutes your workspace and can cause unexpected bugs if two different modules use the exact same function names. 

__Importing Your Own Custom Files:__ Any Pylem source code file you create can be imported into another program as long as it is sitting in the same directory.

```py
## ---
## Step A: Create a file named calculator.pyl

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

## ---
## Step B: Import it into your main script (main.pyl) 

import calculator

result = calculator.add(5, 3)
print(result)  # Output: 8
```

When you trigger an import, Pylem checks locations in a strict priority order:

1. Built-in Modules: Internal core functions compiled directly into Pylem (e.g., `sys`).
2. Current Directory: The folder where your running script lives.
3. `PYLEMPATH`: External folders customized by you or your environment.
4. Standard/Third-Party Library: Core packages and tools installed via a package manager.

__💡 Pro Tip:__ Avoid naming your personal script files the same name as a popular library (like `math.pyl` or `random.pyl`), or Pylem might accidentally import your file instead of the official library, breaking your code.

_[Advanced](#advanced)_

---

[TOC](#table-of-contents)

---

## Reserved Words

The 35 reserved words in Python are also reserved in Pylem:

- `False`, `None`, `True`, `and`, `as`, `assert`, `async`, `await`, `break`, `class`, `continue`, `def`, `del`, `elif`, `else`, `except`, `finally`, `for`, `from`, `global`, `if`, `import`, `in`, `is`, `lambda`, `nonlocal`, `not`, `or`, `pass`, `raise`, `return`, `try`, `while`, `with`, `yield`

There are also new reserved words unique to Pylem:

- [`block`](#block), [`case`](#match--case), [`const`](#constants), [`defer`](#defer), [`enum`](#enum), [`fallthrough`](#fallthrough), [`match`](#match--case), [`mut`](#mutability), [`struct`](#struct), [`type`](#type), [`union`](#union)

---

*This document captures the current state of the Pylem design. The language is still evolving.*

_[Top](#pylem-reference)_
