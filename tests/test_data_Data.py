import os
from contextlib import contextmanager

import pytest
from RIAssigner.data import Data
from RIAssigner.utils import get_extension

from tests.builders import MatchMSDataBuilder, PandasDataBuilder

here = os.path.abspath(os.path.dirname(__file__))


def _add_possible_key(keys, new_keys):
    possible_keys = list(keys)
    possible_keys += new_keys
    return set(possible_keys)


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


@pytest.mark.parametrize("keys", [["test-key"], ["first_key", "second_key"]])
def test_add_possible_keys(keys):
    expected_ri_keys = _add_possible_key(Data._ri_possible_keys, keys)
    expected_rt_keys = _add_possible_key(Data._rt_possible_keys, keys)

    Data.add_possible_ri_keys(keys)
    Data.add_possible_rt_keys(keys)

    assert Data._ri_possible_keys == expected_ri_keys
    assert Data._rt_possible_keys == expected_rt_keys
