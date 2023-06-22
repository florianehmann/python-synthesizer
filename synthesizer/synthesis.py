import numpy as np
from .structures import ADSREnvelope


def calculate_envelope(t: np.ndarray[np.float64], t_press: float, t_release: float, envelope: ADSREnvelope) \
        -> np.ndarray[np.float64]:
    """
    Obtain the normalized envelope factor for given points in time.

    :param t: NumPy array with points in time to evaluate the envelope at.
    :param t_press: Time of the key press.
    :param t_release: Time of the key release.
    :param envelope: Parameters of the Envelope.
    """
    t_peak = t_press + envelope.attack
    t_sustain = t_press + envelope.attack + envelope.decay
    t_end = t_release + envelope.release

    return np.piecewise(
        t,
        condlist=[
            (t_press <= t) & (t < t_peak),
            (t_peak <= t) & (t < t_sustain),
            (t_sustain <= t) & (t < t_release),
            (t_release <= t) & (t < t_end)
        ],
        funclist=[
            lambda tt: (tt - t_press) / envelope.attack,
            lambda tt: - (1 - envelope.sustain) / envelope.decay * (tt - t_peak) + 1,
            lambda tt: envelope.sustain,
            lambda tt: - envelope.sustain / envelope.release * (tt - t_release) + envelope.sustain,
            lambda tt: 0
        ]
    )
