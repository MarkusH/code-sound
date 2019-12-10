import ast
from typing import Generator

from .types import BaseType, Expression, Module, Statement, Assign, For, If, While, Call, Name, Num, Attribute, Tuple


def parse(content: str) -> Generator[BaseType, None, None]:
    tree = ast.parse(content)
    current_type = None
    next_type = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Module):
            next_type = Module()
        elif isinstance(node, ast.Assign):
            next_type = Assign()
        elif isinstance(node, ast.For):
            next_type = For()
        elif isinstance(node, ast.If):
            next_type = If()
        elif isinstance(node, ast.While):
            next_type = While()
        elif isinstance(node, ast.stmt):
            next_type = Statement()
        elif isinstance(node, ast.Call):
            next_type = Call()
        elif isinstance(node, ast.Name):
            next_type = Name()
        elif isinstance(node, ast.Num):
            next_type = Num()
        elif isinstance(node, ast.Attribute):
            next_type = Attribute()
        elif isinstance(node, ast.Tuple):
            next_type = Tuple()
        elif isinstance(node, ast.expr):
            next_type = Expression()

        if current_type is None:
            current_type = next_type

        if current_type.__class__ != next_type.__class__:
            yield current_type
            current_type = next_type

