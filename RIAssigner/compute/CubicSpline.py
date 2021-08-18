from typing import List
from scipy.interpolate import CubicSpline as Model
from RIAssigner.data import Data

from .ComputationMethod import ComputationMethod


class CubicSpline(ComputationMethod):
    def compute(self, query: Data, reference: Data) -> List[Data.RetentionIndexType]:
        """Compute RI using cubic spline interpolation

        Args:
            query (Data): Data for which to compute the retention index
            reference (Data): Reference data with retention time and index

        Returns:
            List[Data.RetentionIndexType]: Computed retention indices
        """
        self._check_data_args(query, reference)

        model = Model(reference.retention_times, reference.retention_indices)
        predicted_ri = model(query.retention_times)
        return predicted_ri.astype(float)
