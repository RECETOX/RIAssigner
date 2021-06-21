import os

import numpy
import pytest
from RIAssigner.data import MatchMSData, PandasData

from .mocks.DataStub import DataStub

here = os.path.abspath(os.path.dirname(__file__))
data_location = os.path.join(here, os.pardir, "data")
data_type_map = {
    ".msp": MatchMSData,
    ".csv": PandasData
}


@pytest.fixture
def reference_alkanes():
    filename = os.path.join(data_location, "csv", "Alkanes_20210325.csv")
    return PandasData(filename, 'min')


@pytest.fixture(params=["aplcms_aligned_peaks.csv", "xcms_variable_metadata.csv", "PFAS_added_rt.msp"])
def queries(request):
    basename, extension = os.path.splitext(request.param)
    filename = os.path.join(data_location, extension[1:], request.param)

    results_path = os.path.join(data_location, "kovats", basename + ".npy")
    expected = numpy.load(results_path)
    return (data_type_map[extension](filename), expected)


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
