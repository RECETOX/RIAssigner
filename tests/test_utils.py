import pytest
import RIAssigner.utils as Utils


@pytest.mark.parametrize("first, second, expected", [[['blub', 'test', 'peter'], ['a', 'b', 'peter', 'd'], 'peter'], [['a'],['b'], None]])
def test_get_first_common_element(first, second, expected):
    actual = Utils.get_first_common_element(first, second)

    assert actual == expected
