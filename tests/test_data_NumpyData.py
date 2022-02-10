import os

import numpy
from RIAssigner.data import NumpyData


def test_constructor():
    actual = NumpyData([0.0, 12.0])
    assert actual is not None
