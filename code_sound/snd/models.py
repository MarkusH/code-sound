from typing import Any, Dict, Generator, Iterable, Optional, Tuple

from ..parser.types import BaseType, Expression, Module, Statement, Assign, If, While, For, Name, Call, Num, Attribute

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


def types_to_sound(code_types: Iterable[BaseType]) -> Generator[Sound, None, None]:
    duration = 0.2
    for code_type in code_types:
        print(code_type)
        if isinstance(code_type, Module):
            yield Sound(Effect("synth", duration, "pl", "D2"), Effect("reverb"))
        elif isinstance(code_type, Statement):
            yield Sound(Effect("synth", duration, "pl", "E2"))
        elif isinstance(code_type, Expression):
            yield Sound(
                Effect("synth", duration, "pl", "F2"),
                Effect("reverb")
            )
        elif isinstance(code_type, Assign):
            yield Sound(
                Effect("synth", duration, "pl", "G2"),
                Effect("reverb")
            )
        elif isinstance(code_type, If):
            yield Sound(
                Effect("synth", duration, "pl", "A2"),
                Effect("reverb")
            )
        elif isinstance(code_type, While):
            yield Sound(
                Effect("synth", duration, "pl", "Bb2"),
                Effect("reverb")
            )
        elif isinstance(code_type, For):
            yield Sound(
                Effect("synth", duration, "pl", "C2"),
                Effect("reverb")
            )
        elif isinstance(code_type, Name):
            yield Sound(
                Effect("synth", duration, "pl", "Bb2"),
                Effect("reverb")
            )
        elif isinstance(code_type, Call):
            yield Sound(
                Effect("synth", duration, "pl", "A2"),
                Effect("reverb")
            )
        elif isinstance(code_type, Num):
            yield Sound(
                Effect("synth", duration, "pl", "C1"),
                Effect("reverb")
            )
        elif isinstance(code_type, Attribute):
            yield Sound(
                Effect("synth", duration, "pl", "G2"),
                Effect("reverb")
            )
