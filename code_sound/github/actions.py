import sys

from code_sound.parser.ast import parse
from code_sound.snd.converter import play
from code_sound.snd.models import types_to_sound


def run_action():
    with open(sys.argv[1]) as fp:
        data = fp.read()

    types = list(parse(data))
    sounds = list(types_to_sound(types))
    play(sounds, "/tmp/outfile.ogg")
    print("::warning Created audio sample")
