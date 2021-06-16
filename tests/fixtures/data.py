import os
import pytest
from RIAssigner.data import PandasData
from RIAssigner.data import MatchMSData


here = os.path.abspath(os.path.dirname(__file__))
data_type_map = {
    ".msp": MatchMSData,
    ".csv": PandasData
}


@pytest.fixture
def reference_alkanes():
    filename = os.path.join(here, os.pardir, "data", "csv", "Alkanes_20210325.csv")
    return PandasData(filename, 'min')


@pytest.fixture(params=["aplcms_aligned_peaks.csv", "xcms_variable_metadata.csv", "PFAS_added_rt.msp"])
def queries(request):
    _, extension = os.path.splitext(request.param)
    filename = os.path.join(here, os.pardir, "data", extension[1:], request.param)

    return data_type_map[extension](filename)
