import ast
from typing import Generator


def parse(content: str) -> Generator[ast.stmt, None, None]:
    tree = ast.parse(content)
    current_type = None
    next_type = None
    for node in ast.walk(tree):
        next_type = node

        if current_type is None:
            current_type = next_type

        if current_type.__class__ != next_type.__class__:
            yield current_type
            current_type = next_type