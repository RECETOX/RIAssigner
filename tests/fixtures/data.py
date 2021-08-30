import os

import numpy
import pytest
from RIAssigner.data import Data, MatchMSData, PandasData
from RIAssigner.utils import get_extension

from .mocks.DataStub import DataStub

here = os.path.abspath(os.path.dirname(__file__))
data_location = os.path.join(here, os.pardir, "data")
data_type_map = {
    ".msp": MatchMSData,
    ".csv": PandasData,
    ".tsv": PandasData,
}


def load_test_file(filename: str) -> Data:
    extension = get_extension(filename)
    filepath = os.path.join(data_location, extension[1:], filename)
    return _load_data(filepath, extension)


def _load_data(filename: str, extension: str) -> Data:
    filetype = extension[1:]
    return data_type_map[extension](filename, filetype, "sec")


@pytest.fixture
def reference_alkanes():
    filename = os.path.join(data_location, "csv", "Alkanes_20210325.csv")
    return PandasData(filename, 'csv', 'min')


@pytest.fixture(params=["aplcms_aligned_peaks.csv", "xcms_variable_metadata.csv", "PFAS_added_rt.msp"])
def queries(request):
    basename, extension = os.path.splitext(request.param)
    filename = os.path.join(data_location, extension[1:], request.param)

    # Get name of method passed to test fixture using @pytest.mark
    method = request.node.get_closest_marker("method").args[0]

    results_path = os.path.join(data_location, method, basename + ".npy")
    expected = numpy.load(results_path)
    return (_load_data(filename, extension), expected)


@pytest.fixture
def indexed_data():
    retention_times = [3.5, 4.68, 5.12, 7.31, 9.01, 9.08]
    retention_indices = [700, 800, 900, 1000, 1100, 1200]
    return DataStub(retention_times, retention_indices)


@pytest.fixture
def non_indexed_data():
    retention_times = [3.99, 4.21, 4.32, 5.83, 6.55, 7.02, 8.65, 9.05]
    return DataStub(retention_times, [])


@pytest.fixture
def invalid_rt_data():
    retention_times = [-1.0, -0.1, None, 3.99]
    return DataStub(retention_times, [])
