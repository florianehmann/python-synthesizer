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


@dataclass
class Tone:
    """
    A Tone created by a key press.

    Class Attributes:
    - t_padding Time in seconds that pads the tone after the envelope has reached zero again.
    """
    t_padding = 0.1
    t_press: float
    t_release: float
    waveform: Waveform
    envelope: ADSREnvelope

    def t_end(self) -> float:
        """Time in seconds at which the tone has ended."""
        return self.t_release + self.envelope.release + self.t_padding
