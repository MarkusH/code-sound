import struct
import pyaudio
import math
import itertools


p = pyaudio.PyAudio()
sample_rate = 44100

channels = 1

stream = p.open(
    rate=sample_rate, channels=channels, format=pyaudio.paFloat32, output=True
)


def get_note(frequency, duration=1, volume=1):
    step = (4 * math.pi * frequency) / sample_rate
    return b"".join(
        struct.pack("f", math.sin(step * i) * volume)
        for i in range(int(sample_rate * duration))
    )


settings = [
    (-12, -8, 1 / 8, 0.2),
    (-8, -4, 1 / 4, 0.4),
    (-4, 0, 1 / 2, 0.6),
    (0, 4, 1 / 1, 0.8),
    (4, 8, 1 / 2, 1.0),
    (8, 12, 1 / 4, 0.5),
]
notes = b"".join(
    itertools.chain(
        get_note(frequency=440 * (2 ** (1 / 12)) ** i, duration=duration, volume=volume)
        for start, end, duration, volume in settings
        for i in range(start, end)
    )
)

stream.write(notes)
