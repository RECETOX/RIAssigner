import os
import numpy as np

import pytest
from RIAssigner.data import Data
from matchms.utils import load_known_key_conversions

from pint import UnitRegistry, Quantity

here = os.path.abspath(os.path.dirname(__file__))


def test_abc():
    with pytest.raises(TypeError) as exception:
        Data(None)

    message = exception.value.args[0]
    assert exception.typename == "TypeError"
    assert str(message).startswith("Can't instantiate abstract class Data with abstract methods")


@pytest.mark.parametrize("value, unit", [
    # Test cases with single values
    (1.0, "sec"),
    # Test cases with more than 2 elements
    ([1.0, 2.0, 3.0], "sec"),
])
def test_uregistry(value, unit):
    ureg = UnitRegistry().Quantity(value, unit)
    assert isinstance(ureg, Quantity)
    if isinstance(value, (list, tuple)):
        np.testing.assert_array_equal(ureg.magnitude, np.array(value))
    else:
        assert ureg.magnitude == value


@pytest.mark.parametrize("value, unit", [
    # Test cases with None
    ([None], "sec"),
    ((None,), "sec"),
    # Test cases with lists or tuples with None
    ([None, None, None], "sec"),
    ((None, None, None), "sec"),
    ([None, None, None], None),
    ((None, None, None), None),
    # Test cases with lists or tuples with mixed values
    ([1.0, None, 3.0], "sec"),
    ((1.0, None, 3.0), "sec"),
    ([1.0, None, 3.0], None),
    ((1.0, None, 3.0), None),
    ([None, 2.0, None], "sec"),
    ((None, 2.0, None), "sec"),
    ([None, 2.0, None], None),
    ((None, 2.0, None), None),
])
def test_uregistry_with_none(value, unit):
    ureg = UnitRegistry().Quantity(value, unit)
    assert isinstance(ureg, Quantity)
    if isinstance(value, (list, tuple)):
        np.testing.assert_array_equal(ureg.magnitude, np.array(value))
    else:
        assert ureg.magnitude == value
    if None in (value if isinstance(value, (list, tuple)) else [value]):
        with pytest.raises(TypeError):
            ureg + ureg


def test_get_possible_rt_keys_is_list():
    actual = Data.get_possible_rt_keys()
    assert type(actual) == list


@pytest.mark.parametrize("expected", [
    "retention_time",
    "rt"
])
def test_get_possible_rt_keys_has_retention_time(expected):
    actual = Data.get_possible_rt_keys()
    assert expected in actual

def test_get_possible_rt_keys_from_matchms_conversion_table_mapping_to_rt():
    # arrange
    # get keys from matchms that map to retention time
    matchms_key_conversion = load_known_key_conversions() # get mapping from matchms
    matchms_rt_mapping = { key: value for key, value in matchms_key_conversion.items() if value == "retention_time"} # mapping to retention time
    expected = list(matchms_rt_mapping.keys())

    # act
    actual = Data.get_possible_rt_keys()

    # assert
    assert set(expected) <= set(actual)

@pytest.mark.parametrize("keys", [
    ["test-key"], ["first_key", "second_key"]
])
def test_add_possible_rt_keys(keys):
    # arrange
    expected_rt_keys = Data.get_possible_rt_keys()
    expected_rt_keys.append(keys)

    # act
    Data.add_possible_rt_keys(keys)

    # assert
    assert Data.get_possible_rt_keys() == expected_rt_keys
