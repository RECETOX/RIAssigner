from typing import Iterable

from RIAssigner.utils import is_sorted

from .SimpleData import SimpleData
from .Data import Data


class ValidateSimpleData(SimpleData):
    def __init__(self, retention_times: Iterable[float], rt_unit: str, retention_indices: Iterable[float] = None):
        """Constructor for `NumpyData` class.

        Args:
            retention_times (Iterable[float]): Retention time values
        """
        super().__init__(retention_times, rt_unit, retention_indices)
        self._validate_input(retention_times, retention_indices)

        self._read(retention_times, retention_indices)

    def _validate_input(self, retention_times, retention_indices):
        if not isinstance(retention_times, list) or None in retention_times:
            raise TypeError("Retention times must be a list and cannot contain None.")
        if not all(map(Data.is_valid, retention_times)):
            raise ValueError("Retention time data is invalid.")
        if not is_sorted(retention_times):
            raise ValueError("Retention time data has to be sorted.")
        if retention_indices is not None:
            if len(retention_times) != len(retention_indices):
                raise ValueError("Retention times and index data are of different length.")
            if not is_sorted(retention_indices):
                raise ValueError("Retention indices data has to be sorted.")
