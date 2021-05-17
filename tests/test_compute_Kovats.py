import numpy
import pytest
from .mocks.DataStub import DataStub
from .fixtures.data import reference_alkanes, queries
from RIAssigner.compute import Kovats


@pytest.fixture
def indexed_data():
    retention_times = [3.5, 4.68, 5.12, 7.31, 9.01, 9.08]
    retention_indices = [700, 800, 900, 1000, 1100, 1200]
    return DataStub(retention_times, retention_indices)


@pytest.fixture
def non_indexed_data():
    retention_times = [3.99, 4.21, 4.32, 5.83, 6.55, 7.02, 8.65, 9.05]
    return DataStub(retention_times, [])


@pytest.fixture
def invalid_rt_data():
    retention_times = [-1.0, -0.1, None, 3.99]
    return DataStub(retention_times, [])


def test_construct():
    compute = Kovats()
    assert compute is not None


def test_exception_reference_none(non_indexed_data):
    method = Kovats()
    with pytest.raises(AssertionError) as exception:
        method.compute(non_indexed_data, None)

    message = exception.value.args[0]
    assert exception.typename == "AssertionError"
    assert message == "Reference data is 'None'."


def test_exception_query_none(indexed_data):
    method = Kovats()
    with pytest.raises(AssertionError) as exception:
        method.compute(None, indexed_data)

    message = exception.value.args[0]
    assert exception.typename == "AssertionError"
    assert message == "Query data is 'None'."


def test_compute_ri_basic_case(non_indexed_data, indexed_data):
    method = Kovats()

    expected = [741.525424,  760.169492,  769.491525,  932.420091,  965.296804,
                986.757991, 1078.823529, 1157.142857]
    actual = method.compute(non_indexed_data, indexed_data)

    numpy.testing.assert_array_almost_equal(actual, expected)


def test_invalid_rt_has_none_ri(invalid_rt_data, indexed_data):
    method = Kovats()

    expected = [None, None, None, 741.5254237288136]
    actual = method.compute(invalid_rt_data, indexed_data)

    numpy.testing.assert_array_equal(actual, expected)


def test_ref_queries(reference_alkanes, queries):
    method = Kovats()

    actual = method.compute(queries, reference_alkanes)
    assert actual is not None
