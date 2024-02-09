import os
from contextlib import contextmanager

import numpy
import pytest
from RIAssigner.data import Data
from RIAssigner.utils import get_extension

from tests.builders import MatchMSDataBuilder, PandasDataBuilder

here = os.path.abspath(os.path.dirname(__file__))
testdata_dir = os.path.join(here, 'data')


@contextmanager
def does_not_raise():
    yield


@pytest.mark.parametrize("filename, filetype, builder, expectation", [
    ["Alkanes_20210325.msp", "msp", MatchMSDataBuilder, does_not_raise()],
    ["Alkanes_20210325.msp", "csv", MatchMSDataBuilder, pytest.raises(TypeError)],
    ["Alkanes_20210325.dat", "msp", MatchMSDataBuilder, does_not_raise()],
    ["Alkanes_20210325.csv", "msp", MatchMSDataBuilder, pytest.raises(Exception)],
    ["Alkanes_20210325.csv", "csv", PandasDataBuilder, does_not_raise()],
    ["Alkanes_20210325.csv", "msp", PandasDataBuilder, pytest.raises(NotImplementedError)],
    ["aplcms_aligned_peaks.dat", "csv", PandasDataBuilder, does_not_raise()],
    ["Alkanes_20210325.msp", "csv", PandasDataBuilder, pytest.raises(Exception)]
])
def test_filetype(filename, filetype, builder, expectation):
    extension = get_extension(filename)
    filepath = os.path.join(here, "data", extension, filename)
    builder = builder().with_filename(filepath).with_filetype(filetype)

    with expectation:
        builder.build()


@pytest.mark.parametrize("builder, filename_dat, filename_native, rt_unit", [
    [MatchMSDataBuilder(), 'Alkanes_20210325.dat', "Alkanes_20210325.msp", "min"],
    [PandasDataBuilder(), 'aplcms_aligned_peaks.dat', "aplcms_aligned_peaks.csv", "sec"]
])
def test_read_dat(builder, filename_dat, filename_native, rt_unit):
    # arrange
    ext = get_extension(filename_native)
    filename = os.path.join(here, 'data', 'dat', filename_dat)
    builder = builder.with_rt_unit(rt_unit).with_filename(filename)

    # act
    data_dat = builder.build()
    data_native = builder.with_filename(os.path.join(testdata_dir, ext, filename_native)).build()

    # assert
    assert data_dat == data_native


@pytest.mark.parametrize("builder, filename, rt_format, expected", [
    [PandasDataBuilder(), "Alkanes_20210325.csv", 'min', [124.8, 145.8, 165, 184.8, 204, 222.6, 245.4, 268.8, 288, 307.2]],
    [PandasDataBuilder(), "Alkanes_20210325.tsv", 'min', [124.8, 145.8, 165, 184.8, 204, 222.6, 245.4, 268.8, 288, 307.2]],
    [PandasDataBuilder(), "Alkanes_ri.csv", 'min', [124.8, 145.8, 165, 184.8, 204, 222.6, 245.4, 268.8, 288, 307.2]],
    [PandasDataBuilder(), "Alkanes_20210325.csv", 'second', [2.08, 2.43, 2.75, 3.08, 3.4, 3.71, 4.09, 4.48, 4.8, 5.12]],
    [MatchMSDataBuilder(), "Alkanes_20210325.msp", 'min', [124.8, 145.8, 165, 184.8]],
    [MatchMSDataBuilder(), "Alkanes_20210325.msp", 'second', [2.08, 2.43, 2.75, 3.08]]
])
def test_read_rts(builder, filename, rt_format, expected):
    ext = get_extension(filename)
    filepath = os.path.join(testdata_dir, ext, filename)
    data = builder.with_filename(filepath).with_rt_unit(rt_format).build()

    actual = data.retention_times[:10]
    numpy.testing.assert_array_almost_equal(actual, expected)


@pytest.mark.parametrize("builder, filename, expected", [
    [PandasDataBuilder(), "Alkanes_20210325.csv", range(1100, 4100, 100)],
    [PandasDataBuilder(), "Alkanes_20210325.tsv", range(1100, 4100, 100)],
    [PandasDataBuilder(), "Alkanes_ri.csv", range(1100, 4100, 100)],
    [PandasDataBuilder(), "Alkanes_retention_index.csv", range(1100, 4100, 100)]
    #[MatchMSDataBuilder(), "recetox_gc-ei_ms_20201028.msp", [2876, 2886.9, 1827.1, 1832.9, 1844.4, 1501, 1528.3, 2102.7, 2154.5, 2207.5]]
])
def test_read_ris(builder, filename, expected):
    ext = get_extension(filename)
    filepath = os.path.join(testdata_dir, ext, filename)
    data = builder.with_filename(filepath).build()

    actual = data.retention_indices
    numpy.testing.assert_array_almost_equal(actual, expected)
