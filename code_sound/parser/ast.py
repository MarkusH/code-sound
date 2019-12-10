import ast
from typing import Generator

from .types import BaseType, Expression, Module, Statement


def parse(content: str) -> Generator[BaseType, None, None]:
    tree = ast.parse(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.Module):
            yield Module()
        elif isinstance(node, ast.stmt):
            yield Statement()
        elif isinstance(node, ast.expr):
            yield Expression()
