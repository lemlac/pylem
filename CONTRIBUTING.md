# Contributing to Pylem

Thank you for considering contributing to **Pylem**!  
This is an early-stage project, so all forms of help — code, documentation, examples, bug reports, design feedback, or just spreading the word — are extremely valuable. 🌌

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [How to Report Issues](#how-to-report-issues)
- [Submitting Pull Requests](#submitting-pull-requests)
- [Coding Style & Conventions](#coding-style--conventions)
- [Testing](#testing)
- [Documentation](#documentation)
- [Questions?](#questions)

## Code of Conduct

We expect all contributors to be kind, respectful, and constructive. Harassment or toxic behavior of any kind will not be tolerated. Be excellent to each other.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/pylem.git
   cd pylem
   ```
3. Set up the development environment (instructions will be added as the project matures). For now, see the `docs/` folder and any existing setup scripts.

Currently the project is in the **language design + early implementation** phase. The most helpful contributions right now include:
- Implementing language features
- Writing tests and examples
- Improving documentation
- Design discussions around syntax, semantics, or architecture

## Development Workflow

- **Main branch** is the primary development branch.
- Create feature branches from `main`:
  ```bash
  git checkout -b feature/my-awesome-feature
  ```
- Make your changes, then open a Pull Request.

## How to Report Issues

- Use the [GitHub Issues](https://github.com/lemlac/pylem/issues) tracker.
- For bugs, please include:
  - A clear description
  - Steps to reproduce
  - Expected vs actual behavior
  - Code example if possible
- For feature requests or design ideas, label them as `enhancement` or `design`.

## Submitting Pull Requests

1. Ensure your code is clean and well-commented.
2. Add or update tests where relevant.
3. Update documentation if you change language behavior or add features.
4. Make sure the PR description clearly explains what you did and why.
5. Link any related issues.

Small PRs are welcome! You don't need to tackle huge features in one go.

## Coding Style & Conventions

- Follow the style already present in the codebase (once implementation grows).
- For the language reference and docs: Use clear, consistent Markdown with plenty of examples.
- Python-inspired code style where applicable (since the language itself is Python-like).
- Prefer readability and maintainability.

Specific style/linting rules will be added (e.g. `ruff`, `black`, or equivalent) as the implementation language is chosen/finalized.

## Testing

- All new features should come with tests.
- Run the full test suite before submitting a PR (instructions will be provided as testing infrastructure is built).

## Documentation

Improving the language reference (`docs/reference.md`) is one of the highest-leverage contributions right now. Feel free to:
- Fix typos and unclear sections
- Add more examples
- Expand missing parts (e.g. full generics details, FFI, etc.)

## Questions?

- Open a [Discussion](https://github.com/lemlac/pylem/discussions) or an Issue.
- Reach out on the issue tracker — we're happy to help onboard new contributors.

---

**Again, thank you!** Every contribution helps turn Pylem from an idea into a real, useful language.

Happy hacking! 🚀
