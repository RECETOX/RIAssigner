from typing import Iterable, TypeVar


T = TypeVar('T')


def get_first_common_element(first: Iterable[T], second: Iterable[T]) -> T:
    return next(item for item in first if item in second)
