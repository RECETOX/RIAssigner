import argparse
import os.path

import numpy
from RIAssigner.cli import LoadDataAction
from RIAssigner.data import PandasData

from tests.fixtures.data import data_location


def test_create():
    sut = LoadDataAction("", "")
    assert sut is not None


def test_load_data_pandas():
    # Arrange
    filename = os.path.join(data_location, "csv", "Alkanes_20210325.csv")
    expected = PandasData(filename)
    namespace = argparse.Namespace()
    parser = argparse.ArgumentParser()
    sut = LoadDataAction("", "data")

    # Act
    sut(parser, namespace, filename)
    actual = namespace.data

    # Assert
    # TODO: Replace with proper comparison operator once implemented
    numpy.testing.assert_array_almost_equal(actual.retention_times, expected.retention_times)
    numpy.testing.assert_array_almost_equal(actual.retention_indices, expected.retention_indices)
