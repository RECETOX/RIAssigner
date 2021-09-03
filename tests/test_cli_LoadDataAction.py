import argparse

import numpy
import pytest
from RIAssigner.cli import LoadDataAction
from RIAssigner.utils import get_extension

from tests.fixtures.data import load_test_file


def test_create():
    sut = LoadDataAction("", "")
    assert sut is not None


@pytest.mark.parametrize("filename, rt_unit", [
    ["Alkanes_20210325.csv", "min"],
    ["Alkanes_20210325.tsv", "min"],
    ["Alkanes_20210325.msp", "min"]
])
def test_load_data(filename, rt_unit):
    # Arrange
    expected = load_test_file(filename, rt_unit)
    namespace = argparse.Namespace()
    parser = argparse.ArgumentParser()
    sut = LoadDataAction("", "data")

    # Act
    extension = get_extension(filename)
    sut(parser, namespace, [expected.filename, extension, rt_unit])
    actual = namespace.data

    # Assert
    # TODO: Replace with proper comparison operator once implemented
    numpy.testing.assert_array_almost_equal(actual.retention_times, expected.retention_times)
    numpy.testing.assert_array_almost_equal(actual.retention_indices, expected.retention_indices)
