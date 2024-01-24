import numpy as np
import pytest

from tests.builders import SimpleDataBuilder


@pytest.mark.parametrize("retention_times, rt_unit, expected", [
    [[0, 12.0], "sec", [0, 12.0]],
    [[0, 0.5], "min", [0, 30.0]]
])
def test_get_retention_times(retention_times, rt_unit, expected):
    builder = SimpleDataBuilder().with_rt(retention_times).with_rt_unit(rt_unit)
    sut = builder.build()
    actual = sut.retention_times

    np.testing.assert_array_equal(actual, expected)

def test_get_retention_indices():
    expected = [134.5, 245.56, 789]
    builder = SimpleDataBuilder().with_rt([100, 200 ,300]).with_ri(expected)
    sut = builder.build()
    actual = sut.retention_indices
    assert actual == expected    
