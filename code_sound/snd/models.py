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
    sample = 'sin'
    for code_type in code_types:
        print(code_type)
        if isinstance(code_type, ast.Module):
            yield Sound(Effect("synth", duration, sample, "D3"),
			Effect("fade", 0.01, 0, 0.1))
        elif isinstance(code_type, ast.stmt):
            yield Sound(Effect("synth", duration, sample, "Bb3"))
        elif isinstance(code_type, ast.Expression):
            yield Sound(
                Effect("synth", duration, sample, "C3"),
			Effect("fade", 0.01, 0, 0.1))
        elif isinstance(code_type, ast.Assign):
            yield Sound(
                Effect("synth", duration, sample, "Db3"),
			Effect("fade", 0.01, 0, 0.1))
        elif isinstance(code_type, ast.If):
            yield Sound(
                Effect("synth", duration, sample, "Eb3"),
			Effect("fade", 0.01, 0, 0.1))
        elif isinstance(code_type, ast.While):
            yield Sound(
                Effect("synth", duration, sample, "E3"),
			Effect("fade", 0.01, 0, 0.1))
        elif isinstance(code_type, ast.For):
            yield Sound(
                Effect("synth", duration, sample, "F3"),
			Effect("fade", 0.01, 0, 0.1))
        elif isinstance(code_type, ast.Name):
            yield Sound(
                Effect("synth", duration, sample, "Gb3"),
			Effect("fade", 0.01, 0, 0.1))
        elif isinstance(code_type, ast.Call):
            yield Sound(
                Effect("synth", duration, sample, "Ab3"),
			Effect("fade", 0.01, 0, 0.1))
        elif isinstance(code_type, ast.Num):
            yield Sound(
                Effect("synth", duration, sample, "A3"),
			Effect("fade", 0.01, 0, 0.1))
        elif isinstance(code_type, ast.Attribute):
            yield Sound(
                Effect("synth", duration, sample, "B3"),
		Effect("fade", 0.01, 0, 0.1)
            )
        elif isinstance(code_type, ast.FunctionDef):
            yield Sound(Effect("synth", duration, "pl", "Bb3"),
			Effect("fade", 0.01, 0, 0.1))
        elif isinstance(code_type, ast.Import):
            yield Sound(Effect("synth", duration, "pl", "G2"),
			Effect("fade", 0.01, 0, 0.1))
        elif isinstance(code_type, ast.Expr):
            yield Sound(
                Effect("synth", duration, "pl", "F2"),
		Effect("fade", 0.01, 0, 0.1)
            )
        elif isinstance(code_type, ast.stmt):
            yield Sound(Effect("synth", duration, "pl", "E2"),
			Effect("fade", 0.01, 0, 0.1))

