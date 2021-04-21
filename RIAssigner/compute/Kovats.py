import numpy
from typing import List
from RIAssigner.data.Data import Data
from .ComputationMethod import ComputationMethod


class Kovats(ComputationMethod):
    """ Class to compute the Kovats retention index. """

    def compute(self, query: Data, reference: Data) -> List[float]:
        self._check_data_args(query, reference)
        return None

    def _check_data_args(self, query, reference):
        assert query is not None, "Query data is 'None'."
        assert reference is not None, "Reference data is 'None'."
