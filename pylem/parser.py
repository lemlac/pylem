from lark import Lark, Transformer, v_args
from .ast import (
    Program, Assignment, Print, Literal, Variable, BinaryOp, If
)


grammar = r"""
    ?start: statement*

    statement: assignment
             | print_stmt
             | if_stmt

    assignment: "mut"? CNAME "=" expr
    print_stmt: "print" "(" expr ")"

    if_stmt: "if" expr ":" block ("else" ":" block)?

    ?expr: term
         | expr "+" term -> binary_op
         | expr "-" term -> binary_op

    ?term: factor
         | term "*" factor -> binary_op
         | term "/" factor -> binary_op

    ?factor: NUMBER -> literal
           | CNAME -> variable
           | "(" expr ")"

    block: "{" statement* "}"          // bracketed blocks
         | INDENT statement* DEDENT    // indented blocks (Lark handles via %declare)

    %import common (CNAME, NUMBER, WS_INLINE)
    %ignore WS_INLINE

    %declare INDENT DEDENT
"""

parser = Lark(grammar, start='start', parser='lalr', transformer=None, propagate_positions=True)


class ASTTransformer(Transformer):
    @v_args(inline=True)
    def assignment(self, is_mut, name, value):
        return Assignment(name=name, value=value, is_mut=bool(is_mut))

    def print_stmt(self, value):
        return Print(value=value[0])

    def literal(self, value):
        return Literal(value=value)

    def variable(self, value):
        return Variable(name=value)

    def binary_op(self, left, op, right):
        return BinaryOp(left=left, operator=op, right=right)

    def if_stmt(self, condition, then_block, else_block=None):
        return If(condition=condition, then_block=then_block, else_block=else_block)

    def statement(self, children):
        return children[0]

    def start(self, statements):
        return Program(statements=statements)


def parse(source: str) -> Program:
    tree = parser.parse(source)
    return ASTTransformer().transform(tree)