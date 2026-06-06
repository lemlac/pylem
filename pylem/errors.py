class PylemError(Exception):
    """Base class for all Pylem errors."""
    pass


class SyntaxError(PylemError):
    def __init__(self, message: str, line: int = None, column: int = None):
        self.line = line
        self.column = column
        super().__init__(f"SyntaxError: {message}" + (f" at line {line}" if line else ""))


class RuntimeError(PylemError):
    def __init__(self, message: str):
        super().__init__(f"RuntimeError: {message}")


class NameError(PylemError):
    def __init__(self, name: str):
        super().__init__(f"NameError: name '{name}' is not defined")