import numpy
import pytest
from RIAssigner.compute import CubicSpline

from tests.fixtures.data import non_indexed_data, reference_alkanes, queries
from tests.fixtures.mocks.DataStub import DataStub


def test_construct():
    method = CubicSpline()
    assert method is not None


@pytest.mark.parametrize('reference_points, query_points, expected', [
    [[(0, 0), (2.71, 800)], [1.34, 0.001], [395.5719, 0.2952]],
    [[(0, 0), (2.71, 800), (4.5, 1200)], [1.5, 2.9, 4.7], [471.7392, 847.3044, 1238.3477]],
])
def test_simple_computations(reference_points, query_points, expected):
    reference_rt, reference_ri = zip(*reference_points)
    reference = DataStub(list(reference_rt), list(reference_ri))
    query = DataStub(query_points, None)
    method = CubicSpline()

    actual = method.compute(query, reference)
    numpy.testing.assert_array_almost_equal(actual, expected, 4)


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


@pytest.mark.method('cubicspline')
def test_detected_features(reference_alkanes, queries):
    method = CubicSpline()

    data, expected = queries
    actual = method.compute(data, reference_alkanes)
    numpy.testing.assert_array_almost_equal(actual, expected)
