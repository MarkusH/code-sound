import io
import json
import os
import subprocess
from typing import List

from code_sound.parser.ast import parse
from code_sound.snd.converter import play
from code_sound.snd.models import types_to_sound


def get_event_data():
    with open(os.environ["GITHUB_EVENT_PATH"]) as fp:
        return json.load(fp)


def find_files():
    event_data = get_event_data()

    after = event_data["after"]
    before = event_data["before"]

    print(f"Checking for files between {before} and {after}.")
    output = subprocess.check_output(["git", "diff", "--name-only", before, after])
    files = output.decode().splitlines()

    for file in files:
        if file.endswith(".py") and os.path.exists(file):
            yield file


def run(files: List[str], out=None):
    buffer = io.StringIO()
    for file in files:
        with open(file) as fp:
            buffer.write(fp.read())
        buffer.write("\n\n\n")

    if buffer.tell() > 0:
        buffer.seek(0)
    else:
        return

    types = list(parse(buffer.read()))
    sounds = list(types_to_sound(types))
    play(sounds, out)


def run_action():
    os.makedirs(".code_sound", exist_ok=True)
    files = list(find_files())
    if not files:
        print("No Python files modified.")
    else:
        print(f"Building sound over these files: {', '.join(files)}")
        run(files, ".code_sound/outfile.ogg")
        print("Created audio sample.")
