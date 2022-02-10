import numpy as np
import pytest
from RIAssigner.data import SimpleData


def test_constructor():
    actual = SimpleData([0.0, 12.0], "sec")
    assert actual is not None


@pytest.mark.parametrize("retention_times, rt_unit, expected", [
    [[0, 12.0], "sec", [0, 12.0]],
    [[0, 0.5], "min", [0, 30.0]]
])
def test_get_retention_times(retention_times, rt_unit, expected):
    sut = SimpleData(retention_times, rt_unit)
    actual = sut.retention_times

    np.testing.assert_array_equal(actual, expected)