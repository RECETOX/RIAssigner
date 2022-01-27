import numpy
import pytest
from RIAssigner.compute import CubicSpline

from tests.fixtures.mocks import DataStub


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
