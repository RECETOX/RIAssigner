from abc import ABC, abstractmethod
from typing import List

from RIAssigner.data import Data


class ComputationMethod(ABC):

    @abstractmethod
    def compute(self, query: Data, reference: Data) -> List[float]:
        """Abstract method for RI computation

        Args:
            query (Data): Dataset for which to compute the RI
            reference (Data): Dataset with retention times & retention index for reference.

        Returns:
            List[float]: Computed retention indices
        """
        ...

    def _check_data_args(self, query, reference):
        """Checks query and reference data for 'None'.

        Args:
            query (Data): Data for which to compute retention indices
            reference (Data): Retention indexed reference data
        """
        if query is None:
            raise ValueError("Query data is not defined.")
        if reference is None:
            raise ValueError("Reference data is not defined.")

    def __eq__(self, o: object) -> bool:
        return type(o) == type(self)
