import pytest

from RIAssigner.compute import ComputationMethod, CubicSpline, Kovats


@pytest.mark.parametrize('this, other, expected', [
    [CubicSpline(), CubicSpline(), True],
    [Kovats(), Kovats(), True],
    [CubicSpline(), Kovats(), False],
    [Kovats(), object(), False],
    [CubicSpline(), object(), False],
])
def test_equal(this, other, expected):
    actual = (this == other)
    assert actual == expected


def test_abc():
    with pytest.raises(TypeError) as exception:
        method = ComputationMethod()

    message = exception.value.args[0]
    assert exception.typename == "TypeError"
    assert str(message).startswith("Can't instantiate abstract class ComputationMethod with abstract method")
