from os.path import splitext
from typing import Iterable, TypeVar

import numpy

T = TypeVar('T')


def get_first_common_element(first: Iterable[T], second: Iterable[T]) -> T:
    """ Get first common element from two lists.
    Returns 'None' if there are no common elements.
    """
    return next((item for item in first if item in second), None)


def define_separator(filename):
    """ Select separator for data values based on filename extension.
    Returns separator.
    """
    if filename.endswith(".tsv"):
        separator = "\t"
    else:
        separator = ","
    return separator


def get_extension(filename: str):
    """Get extension of filename.

    Args:
        filename (str): Filename for which to get the extension.

    Returns:
        str: Filename extension.
    """
    return splitext(filename)[1][1:]


def is_sorted(values) -> bool:
    """Check if values are sorted in ascending order.

    Args:
        values (Any): Values to check

    Returns:
        bool: True if sorted.
    """
    return numpy.all(values[:-1] <= values[1:])
