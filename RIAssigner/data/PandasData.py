from .Data import Data
from pandas import read_csv
from ..utils import get_first_common_element


class PandasData(Data):
    """ Class to handle data from filetypes which can be imported into a pandas dataframe. """
    _column_names = set(['RT', 'rt', 'rts', 'retention_times', 'retention_time', 'retention', 'time'])

    def read(self, filename: str):
        self._data = read_csv(filename)
        self._find_rt_index()

    def _find_rt_index(self):
        # Find first common element
        self._index = get_first_common_element(self._data.columns, self._column_names)

    @property
    def retention_times(self):
        return self._data[self._index]
