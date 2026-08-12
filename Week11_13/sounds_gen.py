"""
Tiny procedural sound effects for the match animation — a bright chirp for
mutual cooperation, a low buzz for defection. Generated once as real .wav
files (pure stdlib: wave + struct + math, no external assets or packages)
and cached under sounds/, so both the first run and every run after it
just work with nothing to download.
"""
import math
import os
import struct
import wave

SAMPLE_RATE = 44100
SOUND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")
COOP_PATH = os.path.join(SOUND_DIR, "cooperate.wav")
DEFECT_PATH = os.path.join(SOUND_DIR, "defect.wav")


def _envelope(i: int, n: int, attack: float, release: float) -> float:
    """0..1 amplitude envelope so tones fade in/out instead of clicking."""
    if n <= 1:
        return 1.0
    t = i / (n - 1)
    if t < attack:
        return t / attack
    if t > 1 - release:
        return max(0.0, (1 - t) / release)
    return 1.0


def _sine_tone(freq: float, duration: float, volume: float = 0.5,
               attack: float = 0.08, release: float = 0.35):
    n = max(1, int(SAMPLE_RATE * duration))
    for i in range(n):
        t = i / SAMPLE_RATE
        env = _envelope(i, n, attack, release)
        yield math.sin(2 * math.pi * freq * t) * volume * env


def _square_ish_tone(freq: float, duration: float, volume: float = 0.4,
                      attack: float = 0.03, release: float = 0.45):
    """A rougher, buzzier tone (blended square + sine) for the defect cue."""
    n = max(1, int(SAMPLE_RATE * duration))
    for i in range(n):
        t = i / SAMPLE_RATE
        env = _envelope(i, n, attack, release)
        sine = math.sin(2 * math.pi * freq * t)
        square = 1.0 if sine >= 0 else -1.0
        yield (0.55 * square + 0.45 * sine) * volume * env


def _write_wav(path: str, sample_stream) -> None:
    frames = bytearray()
    for sample in sample_stream:
        clamped = max(-1.0, min(1.0, sample))
        frames += struct.pack("<h", int(clamped * 32767))
    with wave.open(path, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(bytes(frames))


def _chain(*generators):
    for gen in generators:
        yield from gen


def ensure_sound_files() -> tuple:
    """Create cooperate.wav / defect.wav under sounds/ if they don't
    already exist. Returns (coop_path, defect_path). Idempotent — safe
    to call on every startup."""
    os.makedirs(SOUND_DIR, exist_ok=True)

    if not os.path.exists(COOP_PATH):
        # A bright, quick two-note upward chirp — friendly "ding".
        coop = _chain(
            _sine_tone(880, 0.06, volume=0.5, attack=0.15, release=0.25),
            _sine_tone(1320, 0.08, volume=0.45, attack=0.1, release=0.55),
        )
        _write_wav(COOP_PATH, coop)

    if not os.path.exists(DEFECT_PATH):
        # A short, low, buzzy blip — a little "uh-oh".
        defect = _square_ish_tone(165, 0.13, volume=0.4)
        _write_wav(DEFECT_PATH, defect)

    return COOP_PATH, DEFECT_PATH