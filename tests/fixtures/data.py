import os

import pytest
from RIAssigner.data import Data
from RIAssigner.utils import get_extension
from tests.builders import MatchMSDataBuilder, PandasDataBuilder

from .mocks.DataStub import DataStub

here = os.path.abspath(os.path.dirname(__file__))
data_location = os.path.join(here, os.pardir, "data")
data_type_map = {
    "msp": MatchMSDataBuilder,
    "csv": PandasDataBuilder,
    "tsv": PandasDataBuilder,
}


def load_test_file(filename: str, rt_unit: str) -> Data:
    extension = get_extension(filename)
    filepath = os.path.join(data_location, extension, filename)
    builder = data_type_map[extension]().with_filename(filepath).with_filetype(extension).with_rt_unit(rt_unit)
    return builder.build()


@pytest.fixture
def reference_alkanes():
    return load_test_file("Alkanes_20210325.csv", "min")


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
