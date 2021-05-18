from .Data import Data
from pandas import read_csv
from typing import Iterable
from ..utils import get_first_common_element


class PandasData(Data):
    """ Class to handle data from filetypes which can be imported into a pandas dataframe. """
    _rt_column_names = set(['RT', 'rt', 'rts', 'retention_times', 'retention_time', 'retention', 'time'])
    _carbon_number_column_names = set(['Carbon_Number'])        

    def read(self):
        """ Load content from file into PandasData object. """
        self._data = read_csv(self._filename)

        self._init_carbon_number_index()
        self._init_rt_column_info()
        self._init_ri_column_info()
        self._init_ri_indices()
        self._sort_by_rt()

    def write(self, filename: str):
        self._data.to_csv(filename, index=False)

    def _init_carbon_number_index(self):
        """ Find key of carbon number column and store it. """
        self._carbon_number_index = get_first_common_element(self._data.columns, self._carbon_number_column_names)

    def _init_rt_column_info(self):
        """ Find key of retention time column and store it. """
        self._rt_index = get_first_common_element(self._data.columns, self._rt_column_names)
        self._rt_position = self._data.columns.tolist().index(self._rt_index)

    def _init_ri_column_info(self):
        """ Initialize retention index column name and set its position next to the retention time column. """
        self._ri_index = 'retention_index'
        self._ri_position = self._rt_position + 1

    def _init_ri_indices(self):
        """ Initialize retention indices to a factor of 100 of carbon numbers or None if carbon numbers are not present. """
        if self._carbon_number_index is not None:
            self._data[self._ri_index] = self._data[self._carbon_number_index] * 100
        else:
            self._data.insert(loc=self._ri_position, column=self._ri_index, value=None)

    def _sort_by_rt(self):
        """ Sort peaks by their retention times. """
        self._data.sort_values(by=self._rt_index, axis=0, inplace=True)

    @property
    def retention_times(self) -> Iterable[Data.RetentionTimeType]:
        """ Get retention times in seconds."""
        return self._data[self._rt_index]

    @property
    def retention_indices(self) -> Iterable[Data.RetentionIndexType]:
        """ Get retention indices from data or computed from carbon numbers. """
        if self._carbon_number_index is not None:
            return self._ri_from_carbon_numbers()
        if not self._data[self._ri_index].isnull().all():
            return self._data[self._ri_index]
        raise KeyError("Dataset does not contain retention indices!")

    def _ri_from_carbon_numbers(self):
        """ Returns the RI of compound based on carbon number. """
        return self._data[self._carbon_number_index] * 100

    @retention_indices.setter
    def retention_indices(self, values: Iterable[int]):
        self._data[self._ri_index] = values
