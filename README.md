# Pylem

**The primordial Python — a Python‑shaped language for high‑performance systems code.**

Pylem blends Python’s clarity with the control, predictability, and speed of a systems language. It keeps the ergonomics you love while adding the tools Python has always lacked: immutability by default, sized numeric types, static arrays, structs, enums, compile‑time evaluation, and a unified interpreter/LLVM‑style compilation pipeline.

Pylem aims to eliminate the **two‑language problem** — the constant need to mix Python with C, Rust, or Cython for performance‑critical work. Write expressive code first, optimize later, without switching languages.

---

## 🚀 Why Pylem?

Python is unmatched for productivity, but it struggles when you need…

- *Predictable performance*
- *Static guarantees*
- *To avoid C/Rust extensions*
- *To compile code without rewriting it*

Pylem solves this by offering:

- **Python‑like syntax** with strong static types
- **Immutable‑by‑default semantics** for safer reasoning
- **Sized integers/floats** (`i32`, `f64`, …)
- **Static arrays** (`arr[T, N]`) and low‑level data layouts
- **`struct`, `enum`, `union`** for systems‑style modeling
- **Compile‑time functions** and `const` evaluation
- **Function overloading** and powerful type inference
- **One codebase** that can be **interpreted or AOT‑compiled**

Pylem is designed to feel familiar to Python developers while giving you the performance headroom of a lower‑level language.

---

## 🧠 Key Features

- **Python‑like syntax**: f‑strings, comprehensions, `def`, `match`, exceptions
- **Mutability control**: immutable by default; opt‑in `mut`
- **Performance types**: `i32`, `f64`, `arr[T, N]`, `chr`, optionals `T?`
- **Generics**: `list[T]`, `struct Vec[T]`, `def process[T](x: T)`
- **Compile‑time programming**: `const` values, CT‑evaluated functions
- **Function overloading** with strong inference
- **Advanced control flow**: labeled blocks, guarded `match`, explicit `fallthrough`
- **Unified execution model**: interpret during development, compile for speed

---

## 🧪 Quick Start

```py
print("Hello, Pylem!")

name = "World"
print(f"Hello, {name}!")

mut counter = 0
counter += 1
print(str(counter))  # 1
```

---

## 📦 Example: Generic Stack

```py
struct Stack[T]:
    items: list[T]

class Stack[T]:
    def __init__(mut self):
        self.items = []
    
    def push(mut self, item: T):
        self.items.append(item)
    
    def pop(mut self) -> T?:
        if len(self.items) > 0:
            return self.items.pop()
        return None

mut stack = Stack[int]()
stack.push(42)
item = stack.pop()
if item != None:
    print(str(item))  # 42
```

---

## 💰 Example: Bank Account

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

---

## 🔍 How Pylem Differs from Python

| Concept | Python | Pylem |
|--------|--------|--------|
| Mutability | Everything mutable | Immutable by default; explicit `mut` |
| Types | Dynamic | Static + sized + inferred |
| Overloading | No | Yes |
| Arrays | Lists only | Static arrays + lists |
| Compilation | Optional via Cython | Built‑in interpreter + AOT |
| Low‑level data | Not exposed | `struct`, `enum`, `union` |

---

## 📚 Documentation

- **Full Language Reference** — [`docs/reference.md`](docs/reference.md)
- Additional examples and design notes in [`docs/`](docs/)

---

## 🛠️ Installation / Building

Pylem is in early development. See the [`docs/`](docs/) folder and repository issues for build instructions and current status.

---

## 🧬 Philosophy

Pylem is inspired by:

- **Python** — clarity and ergonomics
- **Rust/C** — control, safety, predictable performance
- **Mojo** — unifying high‑level and low‑level code

The goal is a language that feels like Python but scales to systems programming without rewriting your codebase.

---

## 🗺️ Roadmap

- [ ] Core interpreter
- [ ] Standard library (collections, numerics, etc.)
- [ ] Generics + interface classes
- [ ] LLVM‑based compiler backend
- [ ] Python & C FFI
- [ ] Tooling: formatter, LSP, package manager

---

## 🤝 Contributing

Contributions of all kinds are welcome — code, docs, examples, or design discussion.  
See [`CONTRIBUTING.md`](CONTRIBUTING.md) or open an issue.

---

**From the primordial substance of code.**  
Questions or ideas? Open an issue!

[MIT License](LICENSE)
