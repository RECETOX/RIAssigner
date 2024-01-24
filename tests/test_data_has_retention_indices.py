import pytest
import os

from .builders import SimpleDataBuilder
from .builders import PandasDataBuilder
from .builders import MatchMSDataBuilder

here = os.path.abspath(os.path.dirname(__file__))
testdata_dir_csv = os.path.join(here, 'data', 'csv')
testdata_dir_msp = os.path.join(here, 'data', 'msp')


@pytest.mark.parametrize("retention_index, expected", [
    ((1.0, 2.0, 3.0), True),
    ((1.0, 2.0, None), False)
])
def test_simple_retention_indices(retention_index, expected):
    data = SimpleDataBuilder().with_ri(retention_index).build()
    assert data.has_retention_indices() == expected


@pytest.mark.parametrize("filename_csv, expected", [
    (os.path.join(testdata_dir_csv, "has_retention_indices_t.csv"), True),
    (os.path.join(testdata_dir_csv, "has_retention_indices_f.csv"), False)
])
def test_pandas_retention_indices(filename_csv, expected):
    data = PandasDataBuilder().with_filename(filename_csv).build()
    assert data.has_retention_indices() == expected


@pytest.mark.parametrize("filename_msp, expected", [
    (os.path.join(testdata_dir_msp, "has_retention_indices_t.msp"), True),
    (os.path.join(testdata_dir_msp, "has_retention_indices_f.msp"), False)
])
def test_matchms_retention_indices(filename_msp, expected):
    data = MatchMSDataBuilder().with_filename(filename_msp).build()
    assert data.has_retention_indices() == expected
