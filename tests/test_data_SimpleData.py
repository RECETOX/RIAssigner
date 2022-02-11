import numpy as np
import pytest
from RIAssigner.data import SimpleData


def test_constructor():
    actual = SimpleData([0.0, 12.0], "sec")
    assert actual is not None

@pytest.mark.parametrize("retention_times, expected", [
    [[None, 45.9],"Invalid retention time data."], # contains None
    [[-24.9, 100.2],"Invalid retention time data."], # contains negative rt
    [["200.3", 56.7],"Invalid retention time data."], # contains string
    [[2056.8, 100], "Retention time data has to be sorted."] # is not sorted
])
def test_exception_invalid_rt(retention_times, expected):
    with pytest.raises(AssertionError) as exception:
        SimpleData(retention_times, "sec")

    message = exception.value.args[0]
    assert message == expected, message


@pytest.mark.parametrize("retention_times, rt_unit, expected", [
    [[0, 12.0], "sec", [0, 12.0]],
    [[0, 0.5], "min", [0, 30.0]]
])
def test_get_retention_times(retention_times, rt_unit, expected):
    sut = SimpleData(retention_times, rt_unit)
    actual = sut.retention_times

    np.testing.assert_array_equal(actual, expected)

def test_get_retention_indices():
    expected = [134.5, 245.56, 789]
    sut = SimpleData([], "sec", expected)
    actual = sut.retention_indices
    assert actual == expected
    
