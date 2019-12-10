import ast
from typing import Any, Dict, Generator, Iterable, Optional, Tuple


SND_FX_ARGS_TYPE = Tuple[Optional[Tuple[Any]], Optional[Dict[str, Any]]]


class Effect:
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def transform(self, fx):
        func = getattr(fx, self.name)
        return func(*self.args, **self.kwargs)


class Sound:
    def __init__(self, *effects):
        self.effects = effects

    def transform(self, fx):
        for effect in self.effects:
            fx = effect.transform(fx)
        return fx


def types_to_sound(code_types: Iterable[ast.stmt]) -> Generator[Sound, None, None]:
    duration = 0.2
    for code_type in code_types:
        print(code_type)
        if isinstance(code_type, ast.Module):
            yield Sound(Effect("synth", duration, "pl", "D2"), Effect("reverb"))
        elif isinstance(code_type, ast.Assign):
            yield Sound(
                Effect("synth", duration, "pl", "G2"),
                Effect("reverb")
            )
        elif isinstance(code_type, ast.If):
            yield Sound(
                Effect("synth", duration, "pl", "A2"),
                Effect("reverb")
            )
        elif isinstance(code_type, ast.While):
            yield Sound(
                Effect("synth", duration, "pl", "Bb2"),
                Effect("reverb")
            )
        elif isinstance(code_type, ast.For):
            yield Sound(
                Effect("synth", duration, "pl", "C2"),
                Effect("reverb")
            )
        elif isinstance(code_type, ast.Name):
            yield Sound(
                Effect("synth", duration, "pl", "Bb2"),
                Effect("reverb")
            )
        elif isinstance(code_type, ast.Call):
            yield Sound(
                Effect("synth", duration, "pl", "A2"),
                Effect("reverb")
            )
        elif isinstance(code_type, ast.Num):
            yield Sound(
                Effect("synth", duration, "pl", "C1"),
                Effect("reverb")
            )
        elif isinstance(code_type, ast.Attribute):
            yield Sound(
                Effect("synth", duration, "pl", "G2"),
                Effect("reverb")
            )
        elif isinstance(code_type, ast.stmt):
            yield Sound(Effect("synth", duration, "pl", "E2"))
        elif isinstance(code_type, ast.Expression):
            yield Sound(
                Effect("synth", duration, "pl", "F2"),
                Effect("reverb")
            )
