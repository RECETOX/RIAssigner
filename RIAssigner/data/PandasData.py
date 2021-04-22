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
        self._set_carbon_number_index()
        self._init_rt_column_info()
        self._init_ri_column_info()
        self._init_ri_indices()

    def _set_carbon_number_index(self):
        self._carbon_number_index = get_first_common_element(self._data.columns, self._carbon_number_column_names)

    def _init_rt_column_info(self):
        self._rt_index = get_first_common_element(self._data.columns, self._rt_column_names)
        self._rt_position = self._data.columns.tolist().index(self._rt_index)

    def _init_ri_column_info(self):
        self._ri_index = "retention_index"
        self._ri_position = self._rt_position + 1

    def _init_ri_indices(self):
        if self._carbon_number_index is not None:
            self._data[self._ri_index] = self._data[self._carbon_number_index] * 100
        else:
            self._data.insert(loc=self._ri_position, column=self._ri_index, value=None)

    @property
    def retention_times(self) -> Iterable[int]:
        return self._data[self._rt_index]

    @property
    def retention_indices(self):
        if not self._data[self._ri_index].isnull().all():
            return self._data[self._rt_index]
        else:
            raise KeyError("Dataset does not contain retention indices!")

    @retention_indices.setter
    def retention_indices(self, values: Iterable[int]):
        self._data[self._ri_index] = values
