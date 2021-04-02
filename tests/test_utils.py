import pytest
import RIAssigner.utils as Utils


@pytest.fixture
def first():
    return ['blub', 'test', 'peter']


@pytest.fixture
def second():
    return ['a', 'b', 'peter', 'd']


def test_get_first_common_element(first, second):
    actual = Utils.get_first_common_element(first, second)
    expected = 'peter'

    assert actual == expected
