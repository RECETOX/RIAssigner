import os
import numpy as np

import pytest
from RIAssigner.data import Data

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
