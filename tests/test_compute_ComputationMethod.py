import pytest
from RIAssigner.compute import ComputationMethod


def test_abc():
    with pytest.raises(TypeError) as exception:
        ComputationMethod()

    message = exception.value.args[0]
    assert exception.typename == "TypeError"
    assert str(message).startswith("Can't instantiate abstract class ComputationMethod with abstract method")
