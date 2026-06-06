# Pylem

**The primordial Python** — A Python-like programming language that bridges rapid development and high-performance systems code. See the [reference](docs/reference.md) doc for details.

## Why Pylem?

Python excels at productivity but falls short for performance-critical workloads. This often leads to the **two-language problem** — mixing Python with C, Rust, or Cython, which adds complexity, FFI overhead, and mental context-switching.

**Pylem** solves this by offering familiar Python syntax with opt-in strictness, performance features, and the ability to interpret *or* compile the same code.

The name comes from **"ylem"** — the hypothetical primordial substance from which all matter in the universe was formed (**Py** + **ylem**). Pylem is designed as the foundational building block for high-performance code that still feels like Python. 🌌

## Key Features

- **Python-like syntax**: f-strings, list comprehensions, `def`, `match`/`case`, `try`/`except`, and more.
- **Mutability control**: Variables are immutable by default. Use the `mut` keyword when needed.
- **Performance types**: Sized integers/floats (`i32`, `f64`), static arrays `arr[T, N]`, `struct`, `enum`, `union`, `chr`, optionals `T?`, and more.
- **Generics**: Python-style square bracket notation (e.g. `list[T]`, `struct Vec[T]`, `def process[T](x: T)`).
- **Compile-time programming**: `const` values and compile-time evaluable functions.
- **Flexible blocks & lambdas**: Multi-line lambdas supported via a dual whitespace + bracket system.
- **Function overloading** + strong type inference.
- **Advanced control flow**: Labeled `block`s, rich `match` with guards and explicit `fallthrough`, labeled `break`/`continue`.

Pylem is in early development. It aims to support both fast interpretation and AOT compilation.

## Quick Start

```py
print("Hello, Pylem!")

name = "World"
print(f"Hello, {name}!")

mut counter = 0
counter += 1
print(counter)  # 1
```

## Example: Generic Stack

```py
struct Stack[T]:
    items: list[T]

class Stack[T]:
    def __init__(mut self):
        self.items = []
    
    def push(mut self, item: T):
        self.items.append(item)
    
    def pop(mut self) -> T?:
        if self.items:
            return self.items.pop()
        return None

mut stack = Stack[int]()
stack.push(42)
print(stack.pop())  # 42
```

## Example: Bank Account

```py
struct BankAccount:
    owner: str
    balance: int

class BankAccount:
    def __init__(mut self, owner: str, balance: int = 0):
        self.owner = owner
        self.balance = balance
        
    def deposit(mut self, amount: int):
        self.balance += amount
        return f"${amount} deposited. New balance: ${self.balance}"

acc = BankAccount("Alex", 100)
print(acc.deposit(50))
```

## Documentation

- **[Full Language Reference](docs/reference.md)** — Complete syntax, semantics, and examples.
- The reference highlights notable differences from Python.

## Installation / Building

Currently a work-in-progress. See the `docs/` folder and repository issues for the latest status and build instructions.

## Philosophy

Pylem prioritizes **familiarity for Python developers** while adding the tools needed for systems-level performance. It draws inspiration from Python (ergonomics), Rust/C (control & safety), and projects like Mojo (unifying high-level and low-level code).

## Roadmap

- [ ] Working interpreter for core features
- [ ] Rich standard library (fast collections, numerics, etc.)
- [ ] Generics implementation and traits
- [ ] Compiler backend (LLVM or similar)
- [ ] Python & C FFI / interop
- [ ] Tooling: formatter, LSP, package manager

## Contributing

Early-stage contributions are very welcome — whether it's code, documentation, examples, or design discussion.

See [CONTRIBUTING.md](CONTRIBUTING.md) or open an issue.

## License

[MIT License](LICENSE)

---

**From the primordial substance of code.**  
Questions, ideas, or feedback? Feel free to open an issue!
