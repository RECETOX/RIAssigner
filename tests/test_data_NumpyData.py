import numpy as np
from RIAssigner.data import NumpyData


def test_constructor():
    actual = NumpyData([0.0, 12.0])
    assert actual is not None


def test_get_retention_times():
    expected = [0, 12.0]
    sut = NumpyData(expected)
    actual = sut.retention_times

    assert actual == expected