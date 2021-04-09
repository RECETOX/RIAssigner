import csv
import numpy
import os
import pytest
from RIAssigner.data import PandasData
from RIAssigner.utils import get_first_common_element


here = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(params=["Alkanes_20210325.csv", "aplcms_aligned_peaks.csv", "xcms_variable_metadata.csv"])
def filename_csv(request):
    return os.path.join(here, "data", "csv", request.param)


@pytest.fixture
def csv_content(filename_csv):
    with open(filename_csv, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        data = list(reader)
    return data


@pytest.fixture
def retention_times(csv_content):
    index = get_first_common_element(csv_content[0].keys(), ["RT", "rt"])
    rts = [float(row[index]) for row in csv_content]
    return rts


def test_none():
    pass


def test_open_csv(filename_csv):
    data = PandasData(filename_csv)
    assert data.filename == filename_csv


def test_read_rts(filename_csv, retention_times):
    data = PandasData(filename_csv)

    actual = data.retention_times
    expected = retention_times
    numpy.testing.assert_array_almost_equal(actual, expected)


@pytest.mark.parametrize("filename, expected", [["Alkanes_20210325.csv", range(110, 410, 10)]])
def test_read_ris(filename, expected):
    filename = os.path.join(here, "data", "csv", filename)
    data = PandasData(filename)

    actual = data.retention_indices
    numpy.testing.assert_array_almost_equal(actual, expected)
