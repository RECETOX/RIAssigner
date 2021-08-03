import argparse

import numpy
import pytest
from RIAssigner.cli import LoadDataAction

from tests.fixtures.data import load_test_file


def test_create():
    sut = LoadDataAction("", "")
    assert sut is not None


@pytest.mark.parametrize("filename", [
    "Alkanes_20210325.csv",
    "Alkanes_20210325.tsv",
    "Alkanes_20210325.msp"
])
def test_load_data(filename):
    # Arrange
    expected = load_test_file(filename)
    namespace = argparse.Namespace()
    parser = argparse.ArgumentParser()
    sut = LoadDataAction("", "data")

    # Act
    sut(parser, namespace, expected.filename)
    actual = namespace.data

    # Assert
    # TODO: Replace with proper comparison operator once implemented
    numpy.testing.assert_array_almost_equal(actual.retention_times, expected.retention_times)
    numpy.testing.assert_array_almost_equal(actual.retention_indices, expected.retention_indices)
