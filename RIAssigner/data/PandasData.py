from .Data import Data


class PandasData(Data):
    """ Class to handle data from filetypes which can be imported into a pandas dataframe. """

    def read(self, filename: str):
        ...
