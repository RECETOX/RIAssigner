import numpy
import pytest
from RIAssigner.compute import Kovats

from tests.fixtures import (indexed_data, invalid_rt_data, non_indexed_data)
from tests.fixtures.mocks import DataStub


def test_compute_ri_basic_case(non_indexed_data, indexed_data):
    method = Kovats()

    expected = [741.525424,  760.169492,  769.491525,  932.420091,  965.296804,
                986.757991, 1078.823529, 1157.142857]
    actual = method.compute(non_indexed_data, indexed_data)

    numpy.testing.assert_array_almost_equal(actual, expected)


def test_missing_alkane():
    ref = DataStub([5.0, 7.0], [1000, 1200])
    query = DataStub([6.0], [None])
    expected = [1100]

    actual = Kovats().compute(query, ref)
    numpy.testing.assert_array_almost_equal(actual, expected)
