import numpy as np
import pytest

from tests.builders import SimpleDataBuilder


@pytest.mark.parametrize("retention_times, retention_indices, expected", [
    [[None, 45.9], None,"Invalid retention time data."], # contains None
    [[-24.9, 100.2], None,"Invalid retention time data."], # contains negative rt
    [["200.3", 56.7], None,"Invalid retention time data."], # contains string
    [[2056.8, 100], None, "Retention time data has to be sorted."], # is not sorted
    [[12.0, 100.9], [100], "Retention time and index data are of different length."],
    [[12.0, 100.9], [200, 100], "Retention index data has to be sorted."]
])
def test_constructor_exception(retention_times, retention_indices, expected):
    with pytest.raises(AssertionError) as exception:
        builder = SimpleDataBuilder().with_rt(retention_times).with_ri(retention_indices)
        builder.build()

    message = exception.value.args[0]
    assert message == expected, message


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
