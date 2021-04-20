from .Data import Data
from matchms import Spectrum
from matchms.importing import load_from_msp
from typing import Optional, Iterable


class MatchMSData(Data):
    """ Class to handle data from filetypes which can be imported using 'matchMS'.

    Currently only supports 'msp'.
    """

    def read(self, filename: str):
        self._read_spectra(filename)
        self._read_retention_times()
        self._read_retention_indices()

    def _read_spectra(self, filename):
        if filename.endswith('.msp'):
            self._spectra = list(load_from_msp(filename))
        else:
            raise NotImplementedError("Currently only supports 'msp'.")

    def _read_retention_times(self):
        """ Read retention times from spectrum metadata. """
        self._retention_times = [safe_read_key(spectrum, 'retentiontime') for spectrum in self._spectra]

    def _read_retention_indices(self):
        """ Read retention indices from spectrum metadata. """
        self._retention_indices = [safe_read_key(spectrum, 'retentionindex') for spectrum in self._spectra]

    @property
    def retention_times(self) -> Iterable[Data.RetentionTimeType]:
        """ Get retention times. """
        return self._retention_times

    @property
    def retention_indices(self) -> Iterable[Data.RetentionIndexType]:
        """ Get retention indices."""
        return self._retention_indices

    @retention_indices.setter
    def retention_indices(self, value: Iterable[Data.RetentionIndexType]):
        raise NotImplementedError()


def safe_read_key(spectrum: Spectrum, key: str) -> Optional[float]:
    """ Read key from spectrum and convert to float or return 'None'.
    Tries to read the given key from the spectrum metadata and convert it to a float.
    In case an exception is thrown or the key is not present, returns 'None'.

    Parameters
    ----------
    spectrum:
        Spectrum from which to read the key.
    key:
        Key to be read from the spectrum metadata.

    Returns
    -------
        Either the key's value converted to float or 'None'.
    """

    value = spectrum.get(key, default=None)
    if value is not None:
        try:
            value = float(value)
        except ValueError:
            # RT is in format that can't be converted to float -> set rt to None
            value = None
    return value
