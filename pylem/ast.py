from dataclasses import dataclass
from typing import Any, Optional, List


@dataclass
class Node:
    pass


# === Statements ===
@dataclass
class Program(Node):
    statements: List[Node]


@dataclass
class Assignment(Node):
    name: str
    value: Node
    is_mut: bool = False


@dataclass
class Print(Node):
    value: Node


@dataclass
class If(Node):
    condition: Node
    then_block: List[Node]
    else_block: Optional[List[Node]] = None


# === Expressions ===
@dataclass
class Literal(Node):
    value: Any


@dataclass
class Variable(Node):
    name: str


@dataclass
class BinaryOp(Node):
    left: Node
    operator: str
    right: Node


# Add more node types as you expand (FunctionDef, Call, Block, etc.)