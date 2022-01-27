import pytest
from RIAssigner.compute import CubicSpline, Kovats

from tests.fixtures import indexed_data, non_indexed_data


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


@pytest.mark.parametrize('method', [Kovats, CubicSpline])
def test_construct(method):
    compute = method()
    assert compute is not None


@pytest.mark.parametrize('method', [Kovats(), CubicSpline()])
def test_exception_reference_none(method, non_indexed_data):
    with pytest.raises(AssertionError) as exception:
        method.compute(non_indexed_data, None)

    message = exception.value.args[0]
    assert exception.typename == "AssertionError"
    assert message == "Reference data is 'None'."


@pytest.mark.parametrize('method', [Kovats(), CubicSpline()])
def test_exception_query_none(method, indexed_data):
    with pytest.raises(AssertionError) as exception:
        method.compute(None, indexed_data)

    message = exception.value.args[0]
    assert exception.typename == "AssertionError"
    assert message == "Query data is 'None'."
