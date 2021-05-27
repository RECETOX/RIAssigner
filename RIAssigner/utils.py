from typing import Iterable, TypeVar


T = TypeVar('T')


def get_first_common_element(first: Iterable[T], second: Iterable[T]) -> T:
    """ Get first common element from two lists.
    Returns 'None' if there are no common elements.
    """
    return next((item for item in first if item in second), None)

def define_separator(filename):
    if filename.endswith(".tsv"):
        separator = "\t"
    else:
        separator = ","
    return separator