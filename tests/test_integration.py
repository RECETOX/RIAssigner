import os

from pandas import read_csv
from RIAssigner.compute import Kovats

from tests.builders import MatchMSDataBuilder, PandasDataBuilder

here = os.path.abspath(os.path.dirname(__file__))
testdata_dir = os.path.join(here, 'data')

def test_integration(tmp_path):
    # Load test data and init computation method
    query_path = os.path.join(testdata_dir, "csv/aplcms_aligned_peaks.csv")
    query = PandasDataBuilder().with_filename(query_path).build()

    reference_path = os.path.join(testdata_dir, "msp/Alkanes_20210325.msp")
    reference = MatchMSDataBuilder().with_filename(reference_path).with_rt_unit("min").build()

    method = Kovats()

    query.retention_indices = method.compute(query, reference)
    out_filename = "peaks_with_rt.csv"
    outpath = os.path.join(tmp_path, out_filename)
    query.write(outpath)

    actual = read_csv(outpath)
    expected_path = os.path.join(testdata_dir, 'integration', out_filename)
    expected = read_csv(expected_path)

    assert actual.equals(expected)
