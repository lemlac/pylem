from .ast import Program, Assignment, Print, Literal, Variable, BinaryOp, If
from .environment import Environment
from .errors import RuntimeError


class Interpreter:
    def __init__(self):
        self.globals = Environment()

    def interpret(self, program: Program):
        self.execute_block(program.statements, self.globals)

    def execute_block(self, statements, env: Environment):
        for stmt in statements:
            self.execute(stmt, env)

    def execute(self, stmt, env: Environment):
        if isinstance(stmt, Assignment):
            value = self.evaluate(stmt.value, env)
            env.define(stmt.name, value, stmt.is_mut)
        elif isinstance(stmt, Print):
            value = self.evaluate(stmt.value, env)
            print(value)
        elif isinstance(stmt, If):
            if self.evaluate(stmt.condition, env):
                self.execute_block(stmt.then_block, env)
            elif stmt.else_block:
                self.execute_block(stmt.else_block, env)
        else:
            raise RuntimeError(f"Unknown statement: {type(stmt)}")

    def evaluate(self, expr, env: Environment):
        if isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, Variable):
            return env.get(expr.name)
        elif isinstance(expr, BinaryOp):
            left = self.evaluate(expr.left, env)
            right = self.evaluate(expr.right, env)
            if expr.operator == "+":
                return left + right
            # Add more operators...
            raise RuntimeError(f"Unknown operator: {expr.operator}")
        raise RuntimeError(f"Unknown expression: {type(expr)}")


# Convenience
def run(source: str):
    from .parser import parse
    program = parse(source)
    interpreter = Interpreter()
    interpreter.interpret(program)