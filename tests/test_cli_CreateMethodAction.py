import pytest
from RIAssigner.cli import create_method
from RIAssigner.compute import CubicSpline, Kovats


@pytest.mark.parametrize("method_name, expected_type", [
    ('kovats', Kovats),
    ('cubicspline', CubicSpline),
])
def test_create_method(method_name, expected_type):
    actual = create_method(method_name)
    assert isinstance(actual, expected_type)


@pytest.mark.parametrize("method_name", ['guessing', 'Kovats'])
def test_exception_on_wrong_keyword(method_name):
    with pytest.raises(ValueError, match="Unsupported method"):
        create_method(method_name)
