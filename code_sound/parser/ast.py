import ast
from typing import Generator


def parse(content: str) -> Generator[ast.AST, None, None]:
    tree = ast.parse(content)
    current_type = None
    next_type = None
    for node in ast.walk(tree):
        next_type = node

        if current_type is None:
            current_type = next_type

        if type(current_type) != type(next_type):
            yield current_type
            current_type = next_type
