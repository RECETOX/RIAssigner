from .Data import Data
from pandas import read_csv
from typing import Iterable
from ..utils import get_first_common_element


class PandasData(Data):
    """ Class to handle data from filetypes which can be imported into a pandas dataframe. """
    _rt_column_names = set(['RT', 'rt', 'rts', 'retention_times', 'retention_time', 'retention', 'time'])
    _carbon_number_column_names = set(['Carbon_Number'])

    def read(self, filename: str):
        """ Load content from file into PandasData object. """
        self._data = read_csv(filename)
        self._init_rt_index()
        self._init_carbon_number_index()

    def _init_carbon_number_index(self):
        """ Find key of carbon number column and store it. """
        self._carbon_number_index = get_first_common_element(self._data.columns, self._carbon_number_column_names)

    def _init_rt_index(self):
        """ Find key of retention time column and store it. """
        self._rt_index = get_first_common_element(self._data.columns, self._rt_column_names)

    @property
    def retention_times(self) -> Iterable[float]:
        """ Get retention times."""
        return self._data[self._rt_index]

    @property
    def retention_indices(self) -> Iterable[float]:
        """ Get retention indices from data or computed from carbon numbers. """
        if self._carbon_number_index is not None:
            return self._ri_from_carbon_numbers()
        raise KeyError("Dataset does not contain retention indices!")

    def _ri_from_carbon_numbers(self):
        """ Returns the RI of compound based on carbon number. """
        return self._data[self._carbon_number_index] * 100

    @retention_indices.setter
    def retention_indices(self, value: Iterable[float]):
        raise NotImplementedError()
