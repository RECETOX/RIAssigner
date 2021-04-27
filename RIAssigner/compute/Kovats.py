from typing import List, Iterable
from RIAssigner.data.Data import Data
from .ComputationMethod import ComputationMethod


class Kovats(ComputationMethod):
    """ Class to compute the Kovats retention index. """

    def compute(self, query: Data, reference: Data) -> List[float]:
        """ Compute non-isothermal Kovats retention index.
        For details see https://webbook.nist.gov/chemistry/gc-ri/.

        Parameters
        ----------
        query:
            Dataset for which to compute retention indices.
        """

        self._check_data_args(query, reference)

        lower_index = 0
        higher_index = 0
        retention_indices = []

        for target_rt in query.retention_times:
            ri = None
            if Data.is_valid(target_rt):
                lower_index, higher_index = _get_bound_indices(target_rt, reference.retention_times, lower_index, higher_index)
                ri = _compute_ri(target_rt, reference, lower_index, higher_index)
            retention_indices.append(ri)

        return retention_indices


def _get_bound_indices(target_rt: float, reference_rts: Iterable[Data.RetentionTimeType], lower_index: int, higher_index: int):
    """ Get the indices of previosly eluting and next eluting reference compounds.
    Retention times in 'Data' objects are sorted in ascending order, so this method assumes
    that 'reference_rt' is sorted in ascending order.

    Parameters
    ----------
    reference_rts
        Retention times of reference compounds.

    """
    while reference_rts[higher_index] < target_rt:
        higher_index += 1
    lower_index = max(lower_index, higher_index - 1)
    return lower_index, higher_index


def _compute_ri(target_rt, reference, lower_index, higher_index):
    term_a = target_rt - reference.retention_times[lower_index]
    term_b = reference.retention_times[higher_index] - reference.retention_times[lower_index]

    ri = 100 * term_a / term_b + reference.retention_indices[lower_index]
    return ri
