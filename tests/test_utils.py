import pytest
import RIAssigner.utils as Utils


@pytest.mark.parametrize("first, second, expected", [[['blub', 'test', 'peter'], ['a', 'b', 'peter', 'd'], 'peter'], [['a'], ['b'], None]])
def test_get_first_common_element(first, second, expected):
    actual = Utils.get_first_common_element(first, second)

    assert actual == expected


@pytest.mark.parametrize("filename, expected", [('test_file.csv', ','), ('test_file.tsv', '\t')])
def test_define_separator(filename, expected):
    actual = Utils.define_separator(filename)

    assert actual == expected