from .Data import Data
from pandas import read_csv


class PandasData(Data):
    """ Class to handle data from filetypes which can be imported into a pandas dataframe. """

    def read(self, filename: str):
        self._data = read_csv(filename)

    @property
    def retention_times(self):
        return self._data['RT']
