import os

import pytest
from pandas import read_csv
from RIAssigner.compute import Kovats

from tests.builders import MatchMSDataBuilder, PandasDataBuilder, SimpleDataBuilder

here = os.path.abspath(os.path.dirname(__file__))
testdata_dir = os.path.join(here, 'data')


@pytest.fixture
def reference():
    reference_path = os.path.join(testdata_dir, "msp/Alkanes_20210325.msp")
    reference = MatchMSDataBuilder().with_filename(reference_path).with_rt_unit("min").build()
    return reference


def test_integration(tmp_path, reference):
    # Load test data and init computation method
    query_path = os.path.join(testdata_dir, "csv/aplcms_aligned_peaks.csv")
    query = PandasDataBuilder().with_filename(query_path).build()

    method = Kovats()

    query.retention_indices = method.compute(query, reference)
    out_filename = "peaks_with_rt.csv"
    outpath = os.path.join(tmp_path, out_filename)
    query.write(outpath)

    actual = read_csv(outpath)
    expected_path = os.path.join(testdata_dir, 'integration', out_filename)
    expected = read_csv(expected_path)

    assert actual.equals(expected)


def test_simple_data(tmp_path, reference):
    query = SimpleDataBuilder().with_rt([120, 160]).build()
    method = Kovats()
    actual = method.compute(query, reference)

    expected = [1057.6923076923076, 1273.9583333333333]
    assert actual == expected