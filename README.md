# Pylem

**The primordial Python** — A Python-like programming language that bridges the gap between rapid development and high-performance systems code.

## Why Pylem?

Python is incredibly productive, but it's not designed for performance-critical work. Many projects end up with the **two-language problem** — writing high-level logic in Python and performance-sensitive parts in C, Rust, or Cython. This creates complexity, FFI overhead, and context-switching costs.

**Pylem** solves this by giving Python developers a familiar syntax with opt-in low-level control, performance features, and the ability to interpret *or* compile the same codebase.

The name comes from **"ylem"** — the hypothetical primordial substance from which all matter in the universe was formed (Py + ylem). Pylem aims to be the foundational building block for high-performance code that feels like Python. 🌌

## Key Features

- **Python-like syntax** with f-strings, list comprehensions, `match`/`case`, `try`/`except`, etc.
- **Mutability control**: Variables are immutable by default. Use `mut` for mutable variables.
- **Performance-oriented types**: Sized integers/floats (`i32`, `f64`), static arrays `arr[T, N]`, `struct`, `enum`, `union`, and more.
- **Compile-time programming**: `const` values and compile-time functions.
- **Flexible blocks & lambdas**: Multi-line lambdas with a clever dual whitespace + bracket system.
- **Function overloading** and powerful type inference.
- **Advanced control flow**: Labeled `block`s, rich `match` with guards, labeled `break`/`continue`.
- **Planned**: Generics, FFI (C/Python interop), AOT compilation, and more.

Pylem is in early stages (v0.1 draft). It will support both interpretation (for fast iteration) and compilation (for speed).

## Quick Start

```py
print("Hello, Pylem!")

name = "World"
print(f"Hello, {name}!")

mut counter = 0
counter += 1
print(counter)  # 1
```

See the full language reference for details.

## Example: Bank Account (Classes + Mutability)

```py
class BankAccount:
    def __init__(mut self, owner: str, balance: int = 0):
        self.owner = owner
        self.balance = balance
        
    def deposit(mut self, amount: int):
        self.balance += amount
        return f"${amount} deposited. New balance: ${self.balance}"

my_account = BankAccount("Alex", 100)
print(my_account.deposit(50))
```

## Installation / Building (Coming Soon)

Currently a work-in-progress. Check back for build instructions, or see the `docs/` folder for the language reference.

## Documentation

- **[Full Language Reference](docs/reference.md)** — Detailed syntax, semantics, and examples.
- Notable differences from Python are highlighted throughout the reference.

## Motivation & Philosophy

Pylem is designed for Python developers who want to write performance-critical code without leaving their comfort zone. It draws inspiration from:

- Python (ergonomics)
- C / Rust (control, performance, types)
- Mojo and similar projects (solving the two-language problem)

We prioritize **familiarity first**, then add strictness and performance knobs where they matter.

## Roadmap

- [ ] Working interpreter
- [ ] Core standard library (fast arrays, numerics, etc.)
- [ ] Compiler backend (LLVM or similar)
- [ ] Generics & traits
- [ ] Tooling (formatter, LSP, package manager)
- [ ] Python/C interop

## Contributing

Contributions are welcome! This is an early-stage project. Feel free to open issues, PRs, or discuss design ideas.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details (create this if needed).

## License

[Choose your license, e.g., MIT, Apache 2.0, etc.]

---

**Made with cosmic ambition.**  
Questions? Ideas? Drop them in the issues!
