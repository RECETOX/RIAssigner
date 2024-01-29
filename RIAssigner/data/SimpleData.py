from copy import copy
from typing import Iterable, Optional


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

        self._validate_input_type(retention_times)

        self._read(retention_times, retention_indices)

    def _validate_input_type(self, retention_times):
        if not isinstance(retention_times, list) or None in retention_times:
            raise TypeError("Retention times must be a list and cannot contain None.")

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

    @property
    def comment(self) -> Iterable[Optional[str]]:
        return None
