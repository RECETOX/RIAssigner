class PandasData:

    """ Class to handle data from filetypes which can be imported into a pandas dataframe. """
    def __init__(self, filename: str):
        self._filename = filename

    @property
    def filename(self):
        return self._filename
