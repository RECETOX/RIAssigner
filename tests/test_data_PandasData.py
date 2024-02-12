import os

import numpy
import pytest
from pandas import read_csv

from tests.builders import PandasDataBuilder

here = os.path.abspath(os.path.dirname(__file__))
testdata_dir = os.path.join(here, 'data', 'csv')


@pytest.fixture(params=[
    "Alkanes_20210325.csv",
    "aplcms_aligned_peaks.csv",
    "xcms_variable_metadata.csv",
    "has_retention_times_t.csv",
    "has_retention_times_f.csv"])
def filename_csv(request):
    return os.path.join(testdata_dir, request.param)


def test_open_csv(filename_csv):
    data = PandasDataBuilder().with_filename(filename_csv).build()
    assert data.filename == filename_csv

def test_open_parquet():
    filename = os.path.join(here, "data", "parquet", "10_qc_16x_dil_milliq.parquet")
    data = PandasDataBuilder().with_filename(filename).with_filetype('parquet').build()
    assert data.filename == filename
    assert len(data.retention_times) == 8482
    assert numpy.isclose(numpy.mean(data.retention_times).magnitude, 342.9571167006089, rtol=1e-09, atol=1e-09)


# tmp_path from https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmp-path-fixture
@pytest.mark.parametrize("filename", ["test_file.csv, test_file.tsv"])
def test_write_new_file(filename_csv, filename, tmp_path):
    filepath = os.path.join(tmp_path, filename)

    data = PandasDataBuilder().with_filename(filename_csv).build()
    data.write(filepath)

    assert os.path.isfile(filepath)


def test_filename_extension_assertion(filename_csv, tmp_path):
    filepath = os.path.join(tmp_path, "test_file.abc")

    with pytest.raises(ValueError) as exception:
        PandasDataBuilder().with_filename(filename_csv).build().write(filepath)

    message = exception.value.args[0]
    assert message == "File extension must be 'csv' or 'tsv'."


def test_assert_written_content(filename_csv, tmp_path):
    data = PandasDataBuilder().with_filename(filename_csv).build()
    filename = os.path.split(filename_csv)[-1]

    filepath = os.path.join(tmp_path, filename)
    data.write(filepath)

    expected = data._data
    actual = read_csv(filepath)

    numpy.array_equal(actual.values, expected.values)


@pytest.mark.parametrize("filename", ["aplcms_aligned_peaks.csv"])
def test_ri_column_was_added(filename):
    filename = os.path.join(testdata_dir, filename)
    data = PandasDataBuilder().with_filename(filename).build()

    assert data._ri_index == 'retention_index'


@pytest.mark.parametrize("filename", ["aplcms_aligned_peaks.csv", "Alkanes_20210325.csv"])
def test_equal(filename):
    filename = os.path.join(testdata_dir, filename)
    actual = PandasDataBuilder().with_filename(filename).build()
    expected = PandasDataBuilder().with_filename(filename).build()

    assert expected == actual


@pytest.mark.parametrize("filename, expected", [
    ["Alkanes_20210325.csv", True],
    ["aplcms_aligned_peaks.csv", True],
    ["xcms_variable_metadata.csv", True],
    ["has_retention_times_t.csv", True],
    ["has_retention_times_f.csv", False]
])
def test_has_retention_times(filename, expected):
    filepath = os.path.join(testdata_dir, filename)
    data = PandasDataBuilder().with_filename(filepath).build()
    assert data.has_retention_times() == expected


@pytest.mark.parametrize("filename, expected", [
    ["Alkanes_20210325.csv", True],
    ["aplcms_aligned_peaks.csv", False],
    ["xcms_variable_metadata.csv", False],
    ["has_retention_indices_t.csv", True],
    ["has_retention_indices_f.csv", False],
])
def test_has_retention_indices(filename, expected):
    filepath = os.path.join(testdata_dir, filename)
    data = PandasDataBuilder().with_filename(filepath).build()
    assert data.has_retention_indices() == expected

def test_clean_pandas_column_names():
    #arrange
    expected = ["rt"]
    builder = PandasDataBuilder().with_filename(os.path.join(testdata_dir, "minimal_unclean_colnames.csv"))
    #act
    actual = list(builder.build()._data.columns)
    #assert
    assert set(expected) <= set(actual)
    