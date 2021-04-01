import csv
import numpy
import os
import pytest
from RIAssigner.data import PandasData


here = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def filename_csv():
    return os.path.join(here, "Alkanes_20210325.csv")


@pytest.fixture
def retention_times(filename_csv):
    with open(filename_csv, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        rts = [float(row["RT"]) for row in reader]
        return rts


def test_none():
    pass


def test_has_filename(filename_csv):
    data = PandasData(filename_csv)
    assert data.filename == filename_csv


def test_has_rts(filename_csv, retention_times):
    data = PandasData(filename_csv)

    actual = data.retention_times
    expected = retention_times
    numpy.testing.assert_array_almost_equal(actual, expected)
