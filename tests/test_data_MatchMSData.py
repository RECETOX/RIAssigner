import os

import numpy
import pytest
from matchms.importing import load_from_msp

from .builders.MatchMSDataBuilder import MatchMSDataBuilder


here = os.path.abspath(os.path.dirname(__file__))
testdata_dir = os.path.join(here, 'data', 'msp')


@pytest.fixture(params=[
    "recetox_gc-ei_ms_20201028.msp",
    # Currently excluded due to having None RT values
    # "MSMS-Neg-Vaniya-Fiehn_Natural_Products_Library_20200109.msp",
    # "MSMS-Neg-PFAS_20200806.msp",
    "PFAS_added_rt.msp"])
def filename_msp(request):
    return os.path.join(testdata_dir, request.param)


@pytest.fixture
def retention_times(filename_msp):
    library = list(load_from_msp(filename_msp))
    retention_times = []
    for spectrum in library:
        rt = spectrum.get('retentiontime', None)
        if rt == '':
            rt = -0.1
        elif isinstance(rt, str):
            try:
                rt = float(rt)
            except ValueError:
                rt = -0.1
        retention_times.append(rt)
    retention_times.sort()
    retention_times = [None if i == -0.1 else i for i in retention_times]
    return retention_times


def test_open_msp(filename_msp):
    data = MatchMSDataBuilder().with_filename(filename_msp).build()
    assert data.filename == filename_msp


def test_read_rts_v1(filename_msp, retention_times):
    data = MatchMSDataBuilder().with_filename(filename_msp).build()

    actual = data.retention_times
    expected = retention_times
    numpy.testing.assert_array_equal(actual, expected)


@pytest.mark.parametrize("filename, rt_format, expected", [
    ["Alkanes_20210325.msp", 'min', [124.8, 145.8, 165, 184.8]],
    ["Alkanes_20210325.msp", 'second', [2.08, 2.43, 2.75, 3.08]]
])
def test_read_rts_v2(filename, rt_format, expected):
    filename = os.path.join(testdata_dir, filename)
    data = MatchMSDataBuilder().with_filename(filename).with_rt_unit(rt_format).build()

    actual = data.retention_times
    numpy.testing.assert_array_almost_equal(actual, expected)


@pytest.mark.parametrize("filename, expected", [
    ["recetox_gc-ei_ms_20201028.msp", [2876, 2886.9, 1827.1, 1832.9, 1844.4, 1501, 1528.3, 2102.7, 2154.5, 2207.5]]])
def test_read_ris(filename, expected):
    filename = os.path.join(testdata_dir, filename)
    data = MatchMSDataBuilder().with_filename(filename).build()

    actual = data.retention_indices[:10]
    numpy.testing.assert_array_almost_equal(actual, expected)


@pytest.mark.parametrize("filename", [
    "recetox_gc-ei_ms_20201028.msp", 
    "Alkanes_20210325.msp",
    "PFAS_added_rt.msp"
])
def test_equal(filename):
    filename = os.path.join(testdata_dir, filename)
    actual = MatchMSDataBuilder().with_filename(filename).build()
    expected = MatchMSDataBuilder().with_filename(filename).build()

    assert expected == actual