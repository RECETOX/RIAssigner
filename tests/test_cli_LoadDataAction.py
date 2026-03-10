import numpy
import pytest
from RIAssigner.cli import load_data
from RIAssigner.utils import get_extension

from tests.fixtures.data import load_test_file


@pytest.mark.parametrize("filename, rt_unit", [
    ["Alkanes_20210325.csv", "min"],
    ["Alkanes_20210325.tsv", "min"],
    ["Alkanes_20210325.msp", "min"]
])
def test_load_data(filename, rt_unit):
    # Arrange
    expected = load_test_file(filename, rt_unit)
    extension = get_extension(filename)

    # Act
    actual = load_data(expected.filename, extension, rt_unit)

    # Assert
    # TODO: Replace with proper comparison operator once implemented
    numpy.testing.assert_array_almost_equal(actual.retention_times, expected.retention_times)
    numpy.testing.assert_array_almost_equal(actual.retention_indices, expected.retention_indices)


def test_load_data_unsupported_filetype():
    with pytest.raises(ValueError, match="Unsupported file type"):
        load_data("somefile.xyz", "xyz", "min")
