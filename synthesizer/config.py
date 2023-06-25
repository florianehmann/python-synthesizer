import os


class Singleton(type):

    def __init__(cls, *args, **kwargs):
        super(Singleton, cls).__init__(*args, **kwargs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instance


class Config(metaclass=Singleton):
    """Singleton class containing configurable parameters."""

    def __init__(self):
        self.SAMPLE_RATE: int = int(os.environ.get('SAMPLE_RATE') or 44100)  # Hz
        self.T_PAD: float = float(os.environ.get('T_PAD') or 0.1)  # s
