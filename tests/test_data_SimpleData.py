import numpy as np
from pint.testing import assert_equal
import pytest

from tests.builders import SimpleDataBuilder
from tests.conftest import Q_


@pytest.mark.parametrize(
    "retention_times, rt_unit, expected",
    [[[0, 12.0], "sec", Q_([0, 12.0], "second")], [[0, 0.5], "min", Q_([0, 30.0], "second")]],
)
def test_get_retention_times(retention_times, rt_unit, expected):
    builder = SimpleDataBuilder().with_rt(retention_times).with_rt_unit(rt_unit)
    sut = builder.build()
    actual = sut.retention_times
    assert_equal(actual, expected)


def test_get_retention_indices():
    expected = [134.5, 245.56, 789]
    builder = SimpleDataBuilder().with_rt([100, 200, 300]).with_ri(expected)
    sut = builder.build()
    actual = sut.retention_indices
    np.testing.assert_allclose(actual, expected)


@pytest.mark.parametrize("retention_times, expected", [([1.0, 2.0, 3.0], True), ([1.0, 2.0, -1], False)])
def test_simple_retention_times(retention_times, expected):
    data = SimpleDataBuilder().with_rt(retention_times).build()
    assert data.has_retention_times() == expected


@pytest.mark.parametrize("retention_index, expected", [((1.0, 2.0, 3.0), True), ((1.0, 2.0, None), False)])
def test_simple_retention_indices(retention_index, expected):
    data = SimpleDataBuilder().with_ri(retention_index).build()
    assert data.has_retention_indices() == expected
