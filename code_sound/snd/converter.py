import shlex
from io import BufferedReader, BufferedWriter
from subprocess import PIPE, Popen
from typing import Iterable

import numpy as np
from pysndfx import AudioEffectsChain
from pysndfx.sndfiles import (FileBufferInput, FileBufferOutput, FilePathInput,
                              FilePathOutput, NumpyArrayInput,
                              NumpyArrayOutput, SoxInput, logger)

from .models import Sound


class NullInput(SoxInput):
    def __init__(self):
        self.channels = 1
        self.cmd_prefix = "-n"


class Sequencer(AudioEffectsChain):
    def new(self):
        self.command.append(":")
        return self

    def synth(self, duration, form, note):
        self.command.extend(["synth", duration, form, note])
        return self

    def fade(self, fade_shape='q', fade_in_len=0.0, fade_stop=0.0, fade_out_len=0.0):
        self.command.extend(["fade", fade_shape, fade_in_len, fade_stop, fade_out_len])
        return self

    def __call__(
        self,
        src,
        dst=np.ndarray,
        sample_in=44100,  # used only for arrays
        sample_out=None,
        encoding_out=None,
        channels_out=None,
        allow_clipping=True,
    ):

        # depending on the input, using the right object to set up the input data
        # arguments
        stdin = None
        if isinstance(src, str):
            infile = FilePathInput(src)
            stdin = src
        elif isinstance(src, np.ndarray):
            infile = NumpyArrayInput(src, sample_in)
            stdin = src
        elif isinstance(src, BufferedReader):
            infile = FileBufferInput(src)
            stdin = infile.data  # retrieving the data from the file reader (np array)
        elif src is None:
            infile = NullInput()
        else:
            infile = None

        # finding out which output encoding to use in case the output is ndarray
        if encoding_out is None and dst is np.ndarray:
            if isinstance(stdin, np.ndarray):
                encoding_out = stdin.dtype.type
            elif isinstance(stdin, str):
                encoding_out = np.float32
        # finding out which channel count to use (defaults to the input file's channel
        # count)
        if channels_out is None:
            channels_out = infile.channels
        if (
            sample_out is None
        ):  # if the output samplerate isn't specified, default to input's
            sample_out = sample_in

        # same as for the input data, but for the destination
        if isinstance(dst, str):
            outfile = FilePathOutput(dst, sample_out, channels_out)
        elif dst is np.ndarray:
            outfile = NumpyArrayOutput(encoding_out, sample_out, channels_out)
        elif isinstance(dst, BufferedWriter):
            outfile = FileBufferOutput(dst, sample_out, channels_out)
        else:
            outfile = None

        cmd = shlex.split(
            " ".join(
                [
                    "sox",
                    "-N",
                    "-V1" if allow_clipping else "-V2",
                    infile.cmd_prefix if infile is not None else "-d",
                    outfile.cmd_suffix if outfile is not None else "-d",
                ]
                + list(map(str, self.command))
            ),
            posix=False,
        )

        logger.debug("Running command : %s" % cmd)
        if isinstance(stdin, np.ndarray):
            stdout, stderr = Popen(
                cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE
            ).communicate(stdin.tobytes(order="F"))
        else:
            stdout, stderr = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()

        if stderr:
            raise RuntimeError(stderr.decode())
        elif stdout:
            outsound = np.fromstring(stdout, dtype=encoding_out)
            if channels_out > 1:
                outsound = outsound.reshape(
                    (channels_out, int(len(outsound) / channels_out)), order="F"
                )
            if isinstance(outfile, FileBufferOutput):
                outfile.write(outsound)
            return outsound


def play(sounds: Iterable[Sound], outfile: str = None):
    fx = Sequencer()
    first = True
    for sound in sounds:
        if not first:
            fx = fx.new()
        else:
            first = False

        fx = sound.transform(fx)

    fx(None, outfile, channels_out=1)
