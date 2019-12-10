import io
import json
import os
import subprocess

from code_sound.parser.ast import parse
from code_sound.snd.converter import play
from code_sound.snd.models import types_to_sound


def get_event_data():
    with open(os.environ["GITHUB_EVENT_PATH"]) as fp:
        return json.load(fp)


def run_action():
    event_data = get_event_data()

    after = event_data["after"]
    before = event_data["before"]

    output = subprocess.check_output(["git", "diff", "--name-only", before, after])
    files = output.decode().splitlines()

    buffer = io.StringIO()
    for file in files:
        if file.endswith(".py") and os.path.exists(file):
            with open(file) as fp:
                buffer.write(fp.read())
            buffer.write("\n\n\n")

    if buffer.tell() > 0:
        buffer.seek(0)
    else:
        return

    types = list(parse(buffer.read()))
    sounds = list(types_to_sound(types))
    os.makedirs(".code_sound", exist_ok=True)
    play(sounds, ".code_sound/outfile.ogg")
    print("::warning Created audio sample")
