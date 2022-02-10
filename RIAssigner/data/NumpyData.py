from typing import Iterable
from .Data import Data
import numpy as np

class NumpyData(Data):
    """Class to handle data from numpy arrays
    """

    def __init__(self, rt: np.array):
        """Constructor for `NumpyData` class.

        Args:
            rt (np.array): Retention time values
        """
        super().__init__(None, None, "sec")
    
    def read(self):
        pass

    def write(self):
        pass

    def retention_indices(self) -> Iterable[Data.RetentionIndexType]:
        return super().retention_indices

    def retention_times(self) -> Iterable[Data.RetentionTimeType]:
        return super().retention_times