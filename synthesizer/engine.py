import numpy as np
from .structures import ADSREnvelope, Waveform


class Tone:
    """
    A Tone created by a key press.

    Class Attributes:
    - t_padding Time in seconds that pads the tone after the envelope has reached zero again.
    """
    t_padding = 0.1

    def __init__(self, t_press: float, t_release: float,
                 waveform: Waveform, envelope: ADSREnvelope):
        """
        Create a Tone that is created by a key press.

        :param t_press: Time in seconds at which the key is pressed.
        :param t_release: Time in seconds at which the key is released.
        :param waveform: Underlying waveform of the key.
        :param envelope: Envelope of the tone.
        """
        self.t_press = t_press
        self.t_release = t_release
        self.waveform = waveform
        self.envelope = envelope

    def t_end(self) -> float:
        """Time in seconds at which the tone has ended."""
        return self.t_release + self.envelope.release + self.t_padding

    def __call__(self, t: float) -> float:
        return 0  # TODO
