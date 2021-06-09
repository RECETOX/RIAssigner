import csv
import os

import numpy
from pandas import read_csv
import pytest
from RIAssigner.utils import get_first_common_element

from .builders.PandasDataBuilder import PandasDataBuilder


here = os.path.abspath(os.path.dirname(__file__))
testdata_dir = os.path.join(here, 'data', 'csv')


@pytest.fixture(params=["Alkanes_20210325.csv", "aplcms_aligned_peaks.csv", "xcms_variable_metadata.csv"])
def filename_csv(request):
    return os.path.join(testdata_dir, request.param)


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
    rts.sort()
    return rts


def test_none():
    pass


def test_open_csv(filename_csv):
    data = PandasDataBuilder().with_filename(filename_csv).build()
    assert data.filename == filename_csv


@pytest.mark.parametrize("filename, rt_format, expected", [
    ["Alkanes_20210325.csv", 'min', [124.8, 145.8, 165, 184.8, 204, 222.6, 245.4, 268.8, 288, 307.2]],
    ["Alkanes_20210325.csv", 'second', [2.08, 2.43, 2.75, 3.08, 3.4, 3.71, 4.09, 4.48, 4.8, 5.12]]
])
def test_read_rts(filename, rt_format, expected):
    filename = os.path.join(testdata_dir, filename)
    data = PandasDataBuilder().with_filename(filename).with_rt_unit(rt_format).build()

    actual = data.retention_times[:10]
    numpy.testing.assert_array_almost_equal(actual, expected)


@pytest.mark.parametrize("filename, expected", [["Alkanes_20210325.csv", range(1100, 4100, 100)]])
def test_read_ris(filename, expected):
    filename = os.path.join(testdata_dir, filename)
    data = PandasDataBuilder().with_filename(filename).build()

    actual = data.retention_indices
    numpy.testing.assert_array_almost_equal(actual, expected)


# tmp_path from https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmp-path-fixture
@pytest.mark.parametrize("filename", ["test_file.csv, test_file.tsv"])
def test_write_new_file(filename_csv, filename, tmp_path):
    filepath = os.path.join(tmp_path, filename)
    
    data = PandasDataBuilder().with_filename(filename_csv).build()
    data.write(filepath)

    assert os.path.isfile(filepath)


def test_filename_extension_assertion(filename_csv, tmp_path):
    filepath = os.path.join(tmp_path, "test_file.abc")

    with pytest.raises(AssertionError) as exception:
        PandasDataBuilder().with_filename(filename_csv).build().write(filepath)

    message = exception.value.args[0]
    assert message == "File extention must be 'csv' or 'tsv'."


def test_assert_written_content(filename_csv, tmp_path):
    data = PandasDataBuilder().with_filename(filename_csv).build()
    filename = os.path.split(filename_csv)[-1]

    filepath = os.path.join(tmp_path, filename)
    data.write(filepath)

    expected = data._data
    actual = read_csv(filepath)

    numpy.array_equal(actual.values, expected.values)
