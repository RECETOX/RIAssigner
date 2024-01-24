import os

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

#TODO: first test simple value and unit, then test array and unit, then test None and unit, None and None, Array of None and None, mixed array and unit
@pytest.mark.parametrize("magnitude, unit", [
    (1.0, "sec"),
    ([1.0, 2.0, 3.0], "sec"),
    (1.0, None),
    ([None, None, None], None),
    ([1.0, 2.0, 3.0], None),
    ([1.0, None, None], "sec"),
    ([1.0, None, 3.0], None)
  ])
def test_uregistry(magnitude, unit):
    ureg = UnitRegistry().Quantity(magnitude, unit)
    assert isinstance(ureg, Quantity)

@pytest.mark.parametrize("magnitude, unit", [
    (None, "sec"),
    (None, None)
  ])
def test_uregistry_exceptions(magnitude, unit):
    with pytest.raises(TypeError) as exception:
        UnitRegistry().Quantity(magnitude, unit)

    assert exception.typename == "TypeError"
