import csv
import numpy
import os
import pytest
from RIAssigner.data import PandasData


here = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def filename_csv():
    return os.path.join(here, "data", "Alkanes_20210325.csv")


@pytest.fixture
def csv_content(filename_csv):
    with open(filename_csv, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        data = list(reader)
    return data


@pytest.fixture
def retention_times(csv_content):
    rts = [float(row["RT"]) for row in csv_content]
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
