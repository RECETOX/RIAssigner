import pytest
import pandas as pd
from RIAssigner.data import PandasData, MatchMSData

import os

here = os.path.abspath(os.path.dirname(__file__))
testdata_dir = os.path.join(here, 'data', 'ri_from_comment')

@pytest.fixture
def reference_data_csv(request):
    filename = f'peaks_with_rt_ref_{request.param}.csv'
    df_reference = pd.read_csv(os.path.join(testdata_dir, filename))
    return df_reference['retention_index'].tolist()

@pytest.mark.parametrize("reference_data_csv, comment_string", [("SemiStdNP", "SemiStdNP"), ("StdNP", "StdNP"), ("StdPolar", "StdPolar")], indirect=["reference_data_csv"])
def test_extract_ri_from_csv_comment(reference_data_csv, comment_string):
    query = PandasData(os.path.join(testdata_dir, 'nist_to_ri_2mols.csv'), "csv", rt_unit="seconds")
    query.extract_ri_from_comment(comment_string)
    assert query.retention_indices.tolist() == reference_data_csv

@pytest.fixture
def reference_data_msp(request):
    filename = f'peaks_with_rt_ref_{request.param}_msp.csv'
    df_reference = pd.read_csv(os.path.join(testdata_dir, filename), header=None, usecols=[0])
    comment_parts = df_reference.loc[df_reference[0].str.startswith('COMMENT')][0].str.split()
    comment = [part for sublist in comment_parts for part in sublist]
    ri = [float(part.split('=')[1].split('/')[0]) for part in comment if part.startswith(request.param)]
    return ri

@pytest.mark.parametrize("reference_data_msp, comment_string", [("SemiStdNP", "SemiStdNP"), ("StdNP", "StdNP"), ("StdPolar", "StdPolar")], indirect=["reference_data_msp"])
def test_extract_ri_from_msp_comment(reference_data_msp, comment_string):
    query = MatchMSData(os.path.join(testdata_dir, 'NIST_EI_MS_2mols.msp'), "msp", rt_unit="min")
    query.extract_ri_from_comment(comment_string)
    assert query.retention_indices == reference_data_msp