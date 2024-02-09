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


@pytest.mark.parametrize("filename, expected", [('test_file.csv', 'csv'), ('test_file.tsv', 'tsv')])
def test_get_extension(filename, expected):
    actual = Utils.get_extension(filename)
    assert actual == expected


@pytest.mark.parametrize("values, expected", [
    [[1.2, 4.5, 7.8], True],
    [[0.5, -1.2, 4.5], False]
])
def test_is_sorted(values, expected):
    actual = Utils.is_sorted(values)
    assert actual == expected


@pytest.mark.parametrize("unclean_col_name, expected", [
    [[" col_name_1 "], ["col_name_1"]], # test case for leading and trailing whitespaces
    [["COL_NAME_2"], ["col_name_2"]], # test case for uppercase
    [[" COL_NAME_3 "], ["col_name_3"]], # test case for leading and trailing whitespaces and uppercase
])
def test_clean_column_names(unclean_col_name, expected):
    # arrange and act
    actual = Utils.clean_column_names(unclean_col_name)
    # assert
    assert actual == expected
