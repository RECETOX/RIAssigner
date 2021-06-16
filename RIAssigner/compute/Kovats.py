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

        # Copy rts and ris and insert 0 in the beginning, so that interpolation always starts at 0,0 to the first reference compound.
        reference_rts = list(reference.retention_times)
        reference_ris = list(reference.retention_indices)

        reference_rts.insert(0, 0.0)
        reference_ris.insert(0, 0.0)

        for target_rt in query.retention_times:
            ri = None
            if Data.is_valid(target_rt):
                lower_index, higher_index = _get_bound_indices(target_rt, reference_rts, lower_index, higher_index)
                ri = _compute_ri(target_rt, reference_rts, reference_ris, lower_index, higher_index)
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
    if target_rt > max(reference_rts) or higher_index >= len(reference_rts):
        higher_index = len(reference_rts) - 1
    else:
        while reference_rts[higher_index] < target_rt:
            higher_index += 1
    lower_index = max(lower_index, higher_index - 1)
    return lower_index, higher_index


def _compute_ri(
        target_rt: float,
        reference_rts: Iterable[Data.RetentionTimeType],
        reference_ris: Iterable[Data.RetentionIndexType],
        lower_index: int,
        higher_index: int):
    term_a = target_rt - reference_rts[lower_index]
    term_b = reference_rts[higher_index] - reference_rts[lower_index]

    ri = 100 * term_a / term_b + reference_ris[lower_index]
    return ri
