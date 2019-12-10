from typing import Iterable

from pysndfx import AudioEffectsChain

from .models import Sound


class Sequencer(AudioEffectsChain):
    def new(self):
        self.command.append(":")
        return self

    def synth(self, duration, form, note):
        self.command.extend(["synth", duration, form, note])
        return self


def play(sounds: Iterable[Sound]):
    fx = Sequencer()
    first = True
    for sound in sounds:
        if not first:
            fx = fx.new()
        else:
            first = False

        fx = sound.transform(fx)

    fx(None, None, channels_out=1)
