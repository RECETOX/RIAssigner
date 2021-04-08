from .Data import Data
from matchms.importing import load_from_msp


class MatchMSData(Data):
    """ Class to handle data from filetypes which can be imported using 'matchMS'.

    Currently only supports 'msp'.
    """

    def read(self, filename: str):
        self._spectra = list(load_from_msp(filename))

    @property
    def retention_times(self):
        raise NotImplementedError()

    @property
    def retention_indices(self):
        raise NotImplementedError()
