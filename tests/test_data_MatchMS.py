import os
import numpy
from matchms.importing import load_from_msp
import pytest
from RIAssigner.data import MatchMSData


here = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(params=[
    "recetox_gc-ei_ms_20201028.msp",
    "MSMS-Neg-Vaniya-Fiehn_Natural_Products_Library_20200109.msp",
    "MSMS-Neg-PFAS_20200806.msp",
    "PFAS_added_rt.msp"])
def filename_msp(request):
    return os.path.join(here, "data", "msp", request.param)


@pytest.fixture
def retention_times(filename_msp):
    library = list(load_from_msp(filename_msp))
    retention_times = []
    for spectrum in library:
        rt = spectrum.get('retentiontime', None)
        if rt == '':
            rt = None
        elif isinstance(rt, str):
            try:
                rt = float(rt)
            except ValueError:
                rt = None
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


@pytest.mark.parametrize("filename, expected", [["PFAS_added_rt.msp", [None, 0.45, 1.2, 10.5, 17.4, 188.9]]])
def test_sort_by_rt(retention_times):
    filename = os.path.join(here, "data", "msp", filename)
    data = MatchMSData(filename)

    actual = data.retention_times
    assert actual == expected