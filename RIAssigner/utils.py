from os.path import splitext
from typing import Iterable, TypeVar, List

import numpy

T = TypeVar('T')


def get_first_common_element(first: Iterable[T], second: Iterable[T]) -> T:
    """ Get first common element from two lists.

    Args:
        first (Iterable[T]): First list.
        second (Iterable[T]): Second list.

    Returns:    
        T: First common element or None if no common element is found.
    """
    return next((item for item in first if item in second), None)


def define_separator(filename: str) -> str:
    """ Select separator for data values based on filename extension.

    Args:
        filename (str): Filename for which to get the separator.
    
    Returns:
        str: Separator for data values.
    """
    if filename.endswith(".tsv"):
        separator = "\t"
    else:
        separator = ","
    return separator


def get_extension(filename: str) -> str:
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

def clean_column_names(column_names: List[str]) -> List[str]:
    """ Clean column names by removing leading and trailing whitespaces, converting to lowercase.
    
    Args:
        column_names (List[str]): List of column names to clean.

    Returns:
        List[str]: List of cleaned column names.
    """
    return [name.strip().lower() for name in column_names]
