from copy import copy
from typing import Iterable

from RIAssigner.utils import is_sorted

from .Data import Data


class SimpleData(Data):
    """Class to handle data from numpy arrays
    """

    def __init__(self, retention_times: Iterable[float], rt_unit: str, retention_indices: Iterable[float] = None):
        """Constructor for `NumpyData` class.

        Args:
            retention_times (Iterable[float]): Retention time values
        """
        super().__init__(None, None, rt_unit)
        self._validate_input(retention_times, retention_indices)

        self._read(retention_times, retention_indices)

    def _validate_input(self, retention_times, retention_indices):
        if not all(map(Data.is_valid, retention_times)):
            raise ValueError("Retention time data is invalid.")
        if not is_sorted(retention_times):
            raise ValueError("Retention time data has to be sorted.")
        if retention_indices is not None:
            if len(retention_times) != len(retention_indices):
                raise ValueError("Retention times and index data are of different length.")
            if not is_sorted(retention_indices):
                raise ValueError("Retention indices data has to be sorted.")

    def _read(self, retention_times, retention_indices):
        self._retention_times = Data.URegistry.Quantity(retention_times, self._unit)
        self._retention_indices = copy(retention_indices)

    def write(self):
        raise NotImplementedError("Export of SimpleData is not implemented.")

    @property
    def retention_indices(self) -> Iterable[Data.RetentionIndexType]:
        return copy(self._retention_indices)

    @property
    def retention_times(self) -> Iterable[Data.RetentionTimeType]:
        return self._retention_times.to('seconds')

    @retention_indices.setter
    def retention_indices(self, values: Iterable[Data.RetentionIndexType]):
        raise NotImplementedError()

