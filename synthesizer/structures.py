from dataclasses import dataclass
from enum import Enum, auto
import numpy as np


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

    def __call__(self, t: np.ndarray[np.float64], t_press: float, t_release: float)\
            -> np.ndarray[np.float64]:
        """
        Obtain the normalized envelope factor for given points in time.

        :param t: NumPy array with points in time to evaluate the envelope at.
        :param t_press: Time of the key press.
        :param t_release: Time of the key release.
        """
        t_peak = t_press + self.attack
        t_sustain = t_press + self.attack + self.decay
        t_end = t_release + self.release

        return np.piecewise(
            t,
            condlist=[
                (t_press <= t) & (t < t_peak),
                (t_peak <= t) & (t < t_sustain),
                (t_sustain <= t) & (t < t_release),
                (t_release <= t) & (t < t_end)
            ],
            funclist=[
                lambda tt: (tt - t_press) / self.attack,
                lambda tt: - (1 - self.sustain) / self.decay * (tt - t_peak) + 1,
                lambda tt: self.sustain,
                lambda tt: - self.sustain / self.release * (tt - t_release) + self.sustain,
                lambda tt: 0
            ]
        )


class Waveform(Enum):
    """Underlying Waveform for Tone Generation."""
    SINE = auto()
    TRIANGLE = auto()
    SQUARE = auto()
    NOISE = auto()
