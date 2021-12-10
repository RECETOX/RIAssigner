import os
from contextlib import contextmanager

import pytest
from RIAssigner.data import Data
from RIAssigner.utils import get_extension

from tests.builders import MatchMSDataBuilder, PandasDataBuilder

here = os.path.abspath(os.path.dirname(__file__))


def test_abc():
    with pytest.raises(TypeError) as exception:
        data = Data(None)

    message = exception.value.args[0]
    assert exception.typename == "TypeError"
    assert str(message).startswith("Can't instantiate abstract class Data with abstract methods")


@contextmanager
def does_not_raise():
    yield


@pytest.mark.parametrize("filename, filetype, builder, expectation", [
    ["Alkanes_20210325.msp", "msp", MatchMSDataBuilder, does_not_raise()],
    ["Alkanes_20210325.msp", "csv", MatchMSDataBuilder, pytest.raises(NotImplementedError)],
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


def test_update_possible_keys():
    key = "test-key"

    expected_ri_keys = {'RI', 'ri', 'ris', 'retention_indices', 'retention_index', 'kovats', 'retentionindex', key}
    expected_rt_keys = {'RT', 'rt', 'rts', 'retention_times', 'retention_time', 'retention', 'time', 'retentiontime',
                        key}

    Data.update_possible_ri_keys([key])
    Data.update_possible_rt_keys([key])

    assert Data._ri_possible_keys == expected_ri_keys
    assert Data._rt_possible_keys == expected_rt_keys
