import os
import pytest
from RIAssigner.data import MatchMSData


here = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(params=["recetox_gc-ei_ms_20201028.msp", "MSMS-Neg-Vaniya-Fiehn_Natural_Products_Library_20200109.msp"])
def filename_msp(request):
    return os.path.join(here, "data", request.param)


def test_open_msp(filename_msp):
    data = MatchMSData(filename_msp)
    assert data.filename == filename_msp
