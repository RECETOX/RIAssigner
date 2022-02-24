from typing import List, Iterable
from RIAssigner.data.Data import Data
from .ComputationMethod import ComputationMethod


class Kovats(ComputationMethod):
    """ Class to compute the Kovats retention index. """

    def compute(self, query: Data, reference: Data) -> List[Data.RetentionIndexType]:
        """ Compute non-isothermal Kovats retention index.
        For details see https://webbook.nist.gov/chemistry/gc-ri/.

        Parameters
        ----------
        query:
            Dataset for which to compute retention indices.
        reference:
            Reference dataset with retention times and retention indices

        Returns
        -------
        retention_indices: List[Data.RetentionIndexType]
            List of computed retention indices
        """

        self._check_data_args(query, reference)

        index = 0

        # Copy rts and ris and insert 0 in the beginning, so that interpolation always starts at 0,0 to the first reference compound.
        reference_rts = [0.0] + list(reference.retention_times)
        reference_ris = [0.0] + list(reference.retention_indices)

        retention_indices = [
            self._compute_ri(target_rt, reference_rts, reference_ris, index)
            for target_rt in query.retention_times
        ]

        return retention_indices

    def _compute_ri(self,
                    target_rt: Data.RetentionTimeType,
                    reference_rts: Iterable[Data.RetentionTimeType],
                    reference_ris: Iterable[Data.RetentionTimeType],
                    index: int) -> Data.RetentionIndexType:
        """Compute retention index for target retention time.

        Args:
            target_rt (Data.RetentionTimeType): Retention time for which to compute the index
            reference_rts (Iterable[Data.RetentionTimeType]): Reference retention times
            reference_ris (Iterable[Data.RetentionTimeType]): Reference retention indices
            index (int): Current reference index

        Returns:
            Data.RetentionIndexType: Computed retention index
        """

        ri = None
        if Data.is_valid(target_rt):
            index = _update_index(target_rt, reference_rts, index)
            ri = _compute_kovats(target_rt, reference_rts,
                                 reference_ris, index)
        return ri


def _update_index(target_rt: float, reference_rts: Iterable[Data.RetentionTimeType], index: int):
    """ Get the indices of previosly eluting and next eluting reference compounds.
    Retention times in 'Data' objects are sorted in ascending order, so this method assumes
    that 'reference_rt' is sorted in ascending order.

    Parameters
    ----------
    reference_rts
        Retention times of reference compounds.

    """
    if target_rt > max(reference_rts) or index >= len(reference_rts):
        index = len(reference_rts) - 1
    else:
        while reference_rts[index] < target_rt:
            index += 1
    return index


def _compute_kovats(
        target_rt: float,
        reference_rts: Iterable[Data.RetentionTimeType],
        reference_ris: Iterable[Data.RetentionIndexType],
        index: int) -> float:
    """Compute retention index according to Van den Dool (see https://webbook.nist.gov/chemistry/gc-ri/)

    Args:
        target_rt (float): Retention time for which to compute the RI
        reference_rts (Iterable[Data.RetentionTimeType]): Reference data retention times
        reference_ris (Iterable[Data.RetentionIndexType]): Reference data retention indices
        index (int): Higher index of reference compound (n+1)

    Returns:
        Data.RetentionIndexType: Computed retention index
    """
    term_a = target_rt - reference_rts[index - 1]
    term_b = reference_rts[index] - reference_rts[index - 1]
    factor = reference_ris[index] - reference_ris[index - 1]

    ri = factor * term_a / term_b + reference_ris[index - 1]
    return float(ri)
