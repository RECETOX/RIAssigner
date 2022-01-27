import os

import numpy
import pytest
from matchms.exporting import save_as_msp
from matchms.importing import load_from_msp

from tests.builders import MatchMSDataBuilder

here = os.path.abspath(os.path.dirname(__file__))
testdata_dir = os.path.join(here, 'data', 'msp')


@pytest.fixture(params=[
    "recetox_gc-ei_ms_20201028.msp",
    "Alkanes_20210325.msp",
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


def test_equal(filename_msp):
    actual = MatchMSDataBuilder().with_filename(filename_msp).build()
    expected = MatchMSDataBuilder().with_filename(filename_msp).build()

    assert expected == actual


def test_basic_write(filename_msp, tmp_path):
    # TODO: Reafactor with load_test_file
    data = MatchMSDataBuilder().with_filename(filename_msp).build()

    outpath = os.path.join(tmp_path, "riassigner.msp")
    data.write(outpath)

    spectra = list(load_from_msp(filename_msp))
    spectra.sort(key=lambda spectrum: float(spectrum.get('retentiontime')))

    expected_outpath = os.path.join(tmp_path, "matchms.msp")
    save_as_msp(spectra, expected_outpath)

    with open(expected_outpath, 'r') as file:
        expected = file.readlines()
    with open(outpath, 'r') as file:
        actual = file.readlines()

    assert expected == actual
