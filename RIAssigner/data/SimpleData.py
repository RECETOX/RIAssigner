from typing import Iterable
from .Data import Data
import numpy as np

from copy import copy

class SimpleData(Data):
    """Class to handle data from numpy arrays
    """

    def __init__(self, retention_times: Iterable[float]):
        """Constructor for `NumpyData` class.

        Args:
            rt (np.array): Retention time values
        """
        super().__init__(None, None, "sec")
        self._retention_times = copy(retention_times)
    
    def _read(self):
        pass

    def write(self):
        pass

    @property
    def retention_indices(self) -> Iterable[Data.RetentionIndexType]:
        return super().retention_indices

    @property
    def retention_times(self) -> Iterable[Data.RetentionTimeType]:
        return copy(self._retention_times)