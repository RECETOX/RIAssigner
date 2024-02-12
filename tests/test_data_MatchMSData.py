import os

import numpy
import pytest
from matchms.exporting import save_as_msp
from matchms.importing import load_from_msp

from tests.builders import MatchMSDataBuilder

here = os.path.abspath(os.path.dirname(__file__))
testdata_dir = os.path.join(here, 'data', 'msp')

def rt_or_0(spectrum):
    rt = spectrum.get('retention_time', 0)
    if isinstance(rt, str):
        try:
            rt = float(rt)
        except ValueError:
            rt = 0
    if rt is None:
        rt = 0
    return rt

@pytest.fixture(params=[
    "recetox_gc-ei_ms_20201028.msp",
    "Alkanes_20210325.msp",
    "MSMS-Neg-Vaniya-Fiehn_Natural_Products_Library_20200109.msp",
    "MSMS-Neg-PFAS_20200806.msp",
    "PFAS_added_rt.msp"])
def filename_msp(request):
    return os.path.join(testdata_dir, request.param)


@pytest.fixture
def retention_times(filename_msp):
    library = list(load_from_msp(filename_msp))
    retention_times = []
    for spectrum in library:
        rt = rt_or_0(spectrum)
        retention_times.append(rt)
    retention_times.sort()
    return retention_times


def test_open_msp(filename_msp):
    data = MatchMSDataBuilder().with_filename(filename_msp).build()
    assert data.filename == filename_msp


def test_read_rts_v1(filename_msp, retention_times):
    data = MatchMSDataBuilder().with_filename(filename_msp).build()

    actual = data.retention_times
    expected = retention_times
    numpy.testing.assert_array_equal(actual, expected)


def test_equal(filename_msp):
    actual = MatchMSDataBuilder().with_filename(filename_msp).build()
    expected = MatchMSDataBuilder().with_filename(filename_msp).build()

    assert expected == actual


def test_basic_write(filename_msp, tmp_path):
    # load into MatchMSData and write back
    data = MatchMSDataBuilder().with_filename(filename_msp).build()
    outpath = os.path.join(tmp_path, "riassigner.msp")
    data.write(outpath)

    # load spectra with matchms, sort by rt and write back
    spectra = list(load_from_msp(filename_msp))
    spectra.sort(key=rt_or_0)
    expected_outpath = os.path.join(tmp_path, "matchms.msp")
    save_as_msp(spectra, expected_outpath)

    #check if they match after loading with matchms
    expected = list(load_from_msp(expected_outpath))
    actual = list(load_from_msp(outpath))
    assert expected == actual


@pytest.mark.parametrize("filename, expected", [
    ["recetox_gc-ei_ms_20201028.msp", False],
    ["Alkanes_20210325.msp", True],
    ["MSMS-Neg-Vaniya-Fiehn_Natural_Products_Library_20200109.msp", False],
    ["MSMS-Neg-PFAS_20200806.msp", False],
    ["PFAS_added_rt.msp", True],
])
def test_has_retention_times(filename, expected):
    filepath = os.path.join(testdata_dir, filename)
    data = MatchMSDataBuilder().with_filename(filepath).build()
    assert data.has_retention_times() == expected


@pytest.mark.parametrize("filename, expected", [
    ["recetox_gc-ei_ms_20201028.msp", True],
    ["Alkanes_20210325.msp", True],
    ["MSMS-Neg-Vaniya-Fiehn_Natural_Products_Library_20200109.msp", False],
    ["MSMS-Neg-PFAS_20200806.msp", False],
    ["PFAS_added_rt.msp", False],
])
def test_has_retention_indices(filename, expected):
    filepath = os.path.join(testdata_dir, filename)
    data = MatchMSDataBuilder().with_filename(filepath).build()
    assert data.has_retention_indices() == expected