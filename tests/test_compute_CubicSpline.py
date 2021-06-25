import numpy
import pytest
from RIAssigner.compute import CubicSpline

from tests.fixtures.data import indexed_data, non_indexed_data
from tests.fixtures.mocks.DataStub import DataStub


def test_construct():
    method = CubicSpline()
    assert method is not None


@pytest.mark.parametrize('reference_points, query_points, expected', [
    [[(0, 0), (2.71, 800)], [1.34], [395.57195571955725]]
])
def test_simple_computations(reference_points, query_points, expected):
    reference_rt, reference_ri = zip(*reference_points)
    reference = DataStub(list(reference_rt), list(reference_ri))
    query = DataStub(query_points, None)
    method = CubicSpline()

    actual = method.compute(query, reference)
    numpy.testing.assert_array_almost_equal(actual, expected)


def test_exception_reference_none(non_indexed_data):
    method = CubicSpline()
    with pytest.raises(AssertionError) as exception:
        method.compute(non_indexed_data, None)

    message = exception.value.args[0]
    assert exception.typename == "AssertionError"
    assert message == "Reference data is 'None'."


def test_exception_query_none(indexed_data):
    method = CubicSpline()
    with pytest.raises(AssertionError) as exception:
        method.compute(None, indexed_data)

    message = exception.value.args[0]
    assert exception.typename == "AssertionError"
    assert message == "Query data is 'None'."
