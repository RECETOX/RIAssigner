import numpy as np
from RIAssigner.data import SimpleData


def test_constructor():
    actual = SimpleData([0.0, 12.0])
    assert actual is not None


def test_get_retention_times():
    expected = [0, 12.0]
    sut = SimpleData(expected)
    actual = sut.retention_times

    assert actual == expected