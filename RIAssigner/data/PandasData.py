from typing import Iterable

from pandas import read_csv
from RIAssigner.utils import define_separator, get_first_common_element

from .Data import Data


class PandasData(Data):
    """ Class to handle data from filetypes which can be imported into a pandas dataframe. """
    _carbon_number_column_names = set(['Carbon_Number'])

    def __init__(self, filename: str, filetype: str, rt_unit: str):
        super().__init__(filename, filetype, rt_unit)
        self._read()

    def _read(self):
        """ Load content from file into PandasData object. """
        self._read_into_dataframe()

        self._init_carbon_number_index()
        self._init_rt_column_info()
        self._init_ri_column_info()
        self._init_ri_indices()
        self._sort_by_rt()

    def _read_into_dataframe(self):
        """ Read the data from file into dataframe. """
        if(self._filetype in ['csv', 'tsv']):
            self._data = read_csv(self._filename, sep=None, engine="python")
        else:
            raise NotImplementedError("File formats different from ['csv', 'tsv'] are not implemented yet.")

    def write(self, filename: str):
        """ Write data on disk. Currently supports 'csv' and 'tsv' formats. """
        if not filename.endswith((".csv", ".tsv")):
            raise ValueError("File extension must be 'csv' or 'tsv'.")
        separator = define_separator(filename)
        self._data.to_csv(filename, index=False, sep=separator)

    def _init_carbon_number_index(self):
        """ Find key of carbon number column and store it. """
        self._carbon_number_index = get_first_common_element(self._data.columns, self._carbon_number_column_names)

    def _init_rt_column_info(self):
        """ Find key of retention time column and store it. """
        self._rt_index = get_first_common_element(self._data.columns, self._rt_possible_keys)
        self._rt_position = self._data.columns.tolist().index(self._rt_index)

    def _init_ri_column_info(self):
        """ Initialize retention index column name and set its position next to the retention time column. """
        self._ri_index = get_first_common_element(self._data.columns, self._ri_possible_keys)
        if self._ri_index in self._data.columns:
            self._ri_position = self._data.columns.get_loc(self._ri_index)
        else:
            self._ri_index = 'retention_index'
            self._ri_position = None

    def _init_ri_indices(self):
        """ Initialize retention indices to a factor of 100 of carbon numbers or None if carbon numbers are not present. """
        if self._carbon_number_index is not None:
            self._data[self._ri_index] = self._data[self._carbon_number_index] * 100
        elif self._ri_position is None:
            self._ri_position = self._rt_position + 1
            self._data.insert(loc=self._ri_position, column=self._ri_index, value=None)

    def _sort_by_rt(self):
        """ Sort peaks by their retention times. """
        self._data.sort_values(by=self._rt_index, axis=0, inplace=True)

    def __eq__(self, o: object) -> bool:
        """Comparison operator `==`.

        Args:
            o (object): Object to compare with.

        Returns:
            bool: State of equality.
        """
        if not isinstance(o, PandasData):
            return False
        other: PandasData = o

        are_equal = (self.retention_times == other.retention_times).all()
        try:
            are_equal &= (self.retention_indices == other.retention_indices).all()
        except KeyError:
            pass
        are_equal &= self._data.equals(other._data)
        return are_equal

    @property
    def retention_times(self) -> Iterable[Data.RetentionTimeType]:
        """ Get retention times in seconds."""
        values = self._data[self._rt_index].to_numpy()
        return (values * self._unit).to('seconds')

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
        """Setter for `retention_indices` property.

        Args:
            values (Iterable[int]): Values to assign.
        """
        self._data[self._ri_index] = values
