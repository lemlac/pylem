"""
Pylem — The primordial Python programming language
"""

from .interpreter import Interpreter
from .errors import PylemError

__version__ = "0.1.0"
__all__ = ["Interpreter", "PylemError"]