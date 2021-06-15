import pytest
from RIAssigner.data import Data


def test_abc():
    with pytest.raises(TypeError) as exception:
        data = Data(None)

    message = exception.value.args[0]
    assert exception.typename == "TypeError"
    assert str(message).startswith("Can't instantiate abstract class Data with abstract methods")
