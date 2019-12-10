import ast
from typing import Generator, List
import logging

from .types import BaseType, Expression, Module, Statement, Assign, For, If, While, Call, Name, Num, Attribute, Tuple


def parse(content: str) -> List[BaseType]:
    tree = ast.parse(content)
    position = 0
    current_type = None
    next_type = None
    result = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Module):
            next_type = Module(position)
        elif isinstance(node, ast.Assign):
            next_type = Assign(position)
        elif isinstance(node, ast.For):
            next_type = For(position)
        elif isinstance(node, ast.If):
            next_type = If(position)
        elif isinstance(node, ast.While):
            next_type = While(position)
        elif isinstance(node, ast.stmt):
            next_type = Statement(position)
        elif isinstance(node, ast.Call):
            next_type = Call(position)
        elif isinstance(node, ast.Name):
            next_type = Name(position)
        elif isinstance(node, ast.Num):
            next_type = Num(position)
        elif isinstance(node, ast.Attribute):
            next_type = Attribute(position)
        elif isinstance(node, ast.Tuple):
            next_type = Tuple(position)
        elif isinstance(node, ast.expr):
            next_type = Expression(position)

        if current_type is None:
            current_type = next_type

        if current_type.__class__ != next_type.__class__:
            result.append(current_type)
            current_type = next_type

    return result
