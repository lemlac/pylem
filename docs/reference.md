# Pylem Reference

*Version 0.1 (Draft)*

__The Pylem programming language__ is a dialect of Python but less abstract and more low-level like C. There's a gap in the coding landscape. Python is a widely used programming language, but its slow and not meant for performance critical tasks. That's why many libraries use FFI with compiled code — often written in C — to overcome this limitation. But then you need to write a library in 2 or more languages. Pylem aims to fix that. Python developers won't have abandon a familiar syntax to write performance critical code. Pylem will be able to be interpreted and compiled, all within the same language.

Most things will work just like in Python.

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

The first major difference is the keyword `mut`. Variables are immutable by default. Use `mut` to allow a variable to be mutated.

```py
secret_word = "pylem"
mut guess = ""

while guess != secret_word:
    guess = input("Enter the secret word: ").lower()

print("Access granted!")
```

Another key difference is the inclusion of custom data types like in C: `struct`, `enum`, and `union`.

```py
struct BankAccount:
    owner: str
    balance: int

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        
    def deposit(self, amount):
        self.balance += amount
        return f"${amount} deposited. New balance: ${self.balance}"

# Creating an object instance
my_account = BankAccount("Alex", 100)
print(my_account.deposit(50))
```

Lambda functions can have multiple lines. Pylem has special rules using a mix of indentation and commas/closing brackets to know when a lambda function ends.

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

## Reserved Words

The 35 reserved words in Python are also reserved in Pylem:

- `False`, `None`, `True`, `and`, `as`, `assert`, `async`, `await`, `break`, `class`, `continue`, `def`, `del`, `elif`, `else`, `except`, `finally`, `for`, `from`, `global`, `if`, `import`, `in`, `is`, `lambda`, `nonlocal`, `not`, `or`, `pass`, `raise`, `return`, `try`, `while`, `with`, `yield`

There are also new reserved words unique to Pylem:

- `endlambda`, `enum`, `mut`, `struct`, `union`

---

*This document captures the current state of the Pylem design. The language is still evolving.*
