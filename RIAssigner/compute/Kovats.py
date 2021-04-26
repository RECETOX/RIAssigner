from typing import List
from RIAssigner.data.Data import Data
from .ComputationMethod import ComputationMethod


class Kovats(ComputationMethod):
    """ Class to compute the Kovats retention index. """

    def compute(self, query: Data, reference: Data) -> List[float]:
        """ Compute non-isothermal Kovats retention index.
        For details see https://webbook.nist.gov/chemistry/gc-ri/
        """
        self._check_data_args(query, reference)

        lower_index = 0
        higher_index = 0
        retention_indices = []

        for target_rt in query.retention_times:
            lower_index, higher_index = _get_bound_indices(reference, higher_index, target_rt, lower_index)
            ri = _compute_ri(target_rt, reference, lower_index, higher_index)
            retention_indices.append(ri)

        return retention_indices

    def _check_data_args(self, query, reference):
        assert query is not None, "Query data is 'None'."
        assert reference is not None, "Reference data is 'None'."


def _get_bound_indices(reference, higher_index, target_rt, lower_index):
    """ Get the indices of previosly eluting and next eluting reference compounds. """
    while reference.retention_times[higher_index] < target_rt:
        higher_index += 1
    lower_index = max(lower_index, higher_index - 1)
    return lower_index, higher_index


def _compute_ri(target_rt, reference, lower_index, higher_index):
    term_a = target_rt - reference.retention_times[lower_index]
    term_b = reference.retention_times[higher_index] - reference.retention_times[lower_index]

    ri = 100 * term_a / term_b + reference.retention_indices[lower_index]
    return ri
