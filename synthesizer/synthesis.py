import numpy as np
from .structures import ADSREnvelope, Waveform


def calculate_envelope(t: np.ndarray[np.float64], t_press: float, t_release: float, envelope: ADSREnvelope) \
        -> np.ndarray[np.float64]:
    """
    Obtain the normalized envelope factor for given points in time.

    :param t: Timestamps at which to evaluate the envelope.
    :param t_press: Time of the key press.
    :param t_release: Time of the key release.
    :param envelope: Parameters of the Envelope.

    :returns: Array of envelope values at the given timestamps.
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


def calculate_oscillator(t: np.ndarray[np.float64], freq: float, waveform: Waveform) -> np.ndarray[np.float64]:
    """
    Calculates an oscillator waveform.

    :param t: Timestamps of the oscillation.
    :param freq: Frequency of the oscillation.
    :param waveform: Principle waveform of the oscillation.

    :returns: Array containing the waveform values at the given timestamps with values from -1 to 1.

    :raises NotImplementedError: Supplied waveform is not implemented yet.
    :raises ValueError: Incompatible Parameters.
    """
    if freq <= 0:
        raise ValueError("Need positive frequency for oscillation")

    if waveform == Waveform.SINE:
        osc = np.sin(2 * np.pi * freq * t)
    elif waveform == Waveform.TRIANGLE:
        osc = calculate_triangle_oscillation(t, freq)
    elif waveform == Waveform.SQUARE:
        osc = calculate_square_oscillation(t, freq)
    elif waveform == Waveform.NOISE:
        osc = calculate_noise_oscillation(t)
    else:
        raise NotImplementedError(f"Waveform {waveform} not implemented")

    return osc


def calculate_relative_phase(t: np.ndarray[np.float64], freq: float) -> np.ndarray[np.float64]:
    """
    Calculates an array containing the relative phase of the oscillation for given timestamps.

    :param t: Timestamps of the oscillation.
    :param freq: Frequency of the oscillation.

    :returns: Array containing the relative phases at each timestamp ranging from 0 to 1.
    """
    period = 1 / freq
    return t % period / period


def calculate_triangle_oscillation(t: np.ndarray[np.float64], freq: float) -> np.ndarray[np.float64]:
    return calculate_relative_phase(t, freq) * 2 - 1


def calculate_square_oscillation(t: np.ndarray[np.float64], freq: float) -> np.ndarray[np.float64]:
    phase = calculate_relative_phase(t, freq)

    return np.piecewise(
        phase,
        condlist=[
            phase <= 0.5,
            phase > 0.5
        ],
        funclist=[
            lambda tt: 1,
            lambda tt: -1
        ]
    )


def calculate_noise_oscillation(t: np.ndarray[np.float64]) -> np.ndarray[np.float64]:
    return np.random.rand(len(t)) * 2 - 1
