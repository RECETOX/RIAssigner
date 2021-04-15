from .Data import Data
from pandas import read_csv
from typing import Iterable
from ..utils import get_first_common_element


class PandasData(Data):
    """ Class to handle data from filetypes which can be imported into a pandas dataframe. """
    _rt_column_names = set(['RT', 'rt', 'rts', 'retention_times', 'retention_time', 'retention', 'time'])
    _carbon_number_column_names = set(['Carbon_Number'])

    def read(self, filename: str):
        self._data = read_csv(filename)
        self._set_rt_index_n_position()
        self._set_carbon_number_index()

    def _set_carbon_number_index(self):
        self._carbon_number_index = get_first_common_element(self._data.columns, self._carbon_number_column_names)

    def _set_rt_index_n_position(self):
        self._rt_index = get_first_common_element(self._data.columns, self._rt_column_names)
        self._rt_position = self._data.columns.tolist().index(self._rt_index)

    @property
    def retention_times(self) -> Iterable[int]:
        return self._data[self._rt_index]

    @property
    def retention_indices(self):
        if self._carbon_number_index is not None:
            return self._data[self._carbon_number_index] * 10
        raise KeyError("Dataset does not contain retention indices!")

    @retention_indices.setter
    def retention_indices(self, value: Iterable[int]):
        if len(value) == len(self._data):
            self._ri_position = self._rt_position + 1  
            self._data.insert(loc=self._ri_position, column="retention_index", value=value)
        else:
            raise ValueError("There is different numbers of computed indices and peaks.")
