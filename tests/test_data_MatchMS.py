import os
import numpy
from matchms.importing import load_from_msp
import pytest
from RIAssigner.data import MatchMSData
from RIAssigner.data.MatchMSData import safe_read_rt


here = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(params=[
    "recetox_gc-ei_ms_20201028.msp",
    "MSMS-Neg-Vaniya-Fiehn_Natural_Products_Library_20200109.msp",
    "MSDIAL-TandemMassSpectralAtlas-VS68-Neg.msp",
    "MSDIAL-TandemMassSpectralAtlas-VS68-Pos.msp"])
def filename_msp(request):
    return os.path.join(here, "data", "msp", request.param)


@pytest.fixture
def retention_times(filename_msp):
    library = list(load_from_msp(filename_msp))
    retention_times = []
    for spectrum in library:
        rt = safe_read_rt(spectrum)
        retention_times.append(rt)
    return retention_times


def test_open_msp(filename_msp):
    data = MatchMSData(filename_msp)
    assert data.filename == filename_msp


def test_read_rts(filename_msp, retention_times):
    data = MatchMSData(filename_msp)

    actual = data.retention_times
    expected = retention_times
    numpy.testing.assert_array_equal(actual, expected)
