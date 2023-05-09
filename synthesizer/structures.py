from dataclasses import dataclass
from enum import Enum, auto


@dataclass
class ADSREnvelope:
    """
    Parameters of the Envelope.

    Attack, decay and release are in seconds, and Sustain is in percent of the maximum value.
    """
    attack: float
    decay: float
    sustain: float
    release: float


class Waveform(Enum):
    """Underlying Waveform for Tone Generation."""
    SINE = auto()
    TRIANGLE = auto()
    SQUARE = auto()
    NOISE = auto()
