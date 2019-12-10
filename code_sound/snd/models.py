from typing import Any, Dict, Generator, Iterable, Optional, Tuple

from ..parser.types import BaseType, Expression, Module, Statement

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
    for code_type in code_types:
        if isinstance(code_type, Module):
            yield Sound(Effect("synth", 1, "pl", "E2"), Effect("reverb"))
        elif isinstance(code_type, Statement):
            yield Sound(Effect("synth", 1, "pl", "A0"), Effect("pitch", 1200))
        elif isinstance(code_type, Expression):
            yield Sound(
                Effect("synth", 1, "pl", "C1"),
                Effect("reverb"),
                Effect("pitch", 1200),
            )
