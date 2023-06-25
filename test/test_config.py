import os

from synthesizer import Config

EXAMPLE_SAMPLE_RATE = 1234
EXAMPLE_T_PAD = 314.15


def test_instantiate():
    Config()


def test_singleton():
    config1 = Config()
    config2 = Config()
    assert id(config1) == id(config2)


def test_parameter_mutability():
    config1 = Config()
    config1.T_PAD = EXAMPLE_T_PAD

    config2 = Config()

    assert config1.T_PAD == EXAMPLE_T_PAD
    assert config2.T_PAD == EXAMPLE_T_PAD


def test_environment_variables(monkeypatch):
    monkeypatch.setenv('SAMPLE_RATE', str(EXAMPLE_SAMPLE_RATE))
    monkeypatch.setenv('T_PAD', str(EXAMPLE_T_PAD))
    Config().__init__()

    assert Config().SAMPLE_RATE == EXAMPLE_SAMPLE_RATE
    assert Config().T_PAD == EXAMPLE_T_PAD
