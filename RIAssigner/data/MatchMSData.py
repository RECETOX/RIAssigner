from typing import Iterable, Optional

from matchms import Spectrum
from matchms.exporting import save_as_msp
from matchms.importing import load_from_msp
from RIAssigner.utils import get_first_common_element

from .Data import Data


class MatchMSData(Data):
    """ Class to handle data from filetypes which can be imported using 'matchMS'.

    Currently only supports 'msp'.
    """

    def __init__(self, filename: str, filetype: str, rt_unit: str):
        super().__init__(filename, filetype, rt_unit)
        self._read()

    def _read(self):
        """Load data into object and initialize properties.
        """
        self._read_spectra(self._filename, self._filetype)
        self._init_rt_key()
        self._init_ri_key()

        self._sort_spectra_by_rt()

        self._read_retention_times()
        self._read_retention_indices()

    def write(self, filename: str):
        """Write data to back to 'msp' file

        Args:
            filename (str): Path to filename under which to store the data.
        """
        save_as_msp(self._spectra, filename)

    def _read_spectra(self, filename: str, filetype: str):
        """Read spectra from 'msp' file into data.

        Args:
            filename (str): Path to filename from which to load the data.

        Raises:
            NotImplementedError: For filetypes other tahn 'msp'.
        """
        if filetype == 'msp':
            self._spectra = list(load_from_msp(filename))
        else:
            raise NotImplementedError("Currently only supports 'msp'.")

    def _init_rt_key(self):
        """ Identify retention-time key from spectrum metadata. """
        rt_key = get_first_common_element(self._rt_possible_keys, self._spectra[0].metadata.keys())
        self._rt_key = rt_key or 'retentiontime'

    def _init_ri_key(self):
        """ Identify retention-index key from spectrum metadata. """
        ri_key = get_first_common_element(self._ri_possible_keys, self._spectra[0].metadata.keys())
        self._ri_key = ri_key or 'retentionindex'

    def _read_retention_times(self):
        """ Read retention times from spectrum metadata. """
        self._retention_times = Data.URegistry.Quantity([safe_read_key(spectrum, self._rt_key) for spectrum in self._spectra], self._unit)

    def _read_retention_indices(self):
        """ Read retention indices from spectrum metadata. """
        self.retention_indices = [safe_read_key(spectrum, self._ri_key) for spectrum in self._spectra]

    def _sort_spectra_by_rt(self):
        """ Sort objects (peaks) in spectra list by their retention times. """
        self._spectra.sort(key=lambda spectrum: safe_read_key(spectrum, self._rt_key))

    def __eq__(self, o: object) -> bool:
        """Comparison operator `==`.

        Args:
            o (object): Object to compare with.

        Returns:
            bool: State of equality.
        """
        if not isinstance(o, MatchMSData):
            return False
        other: MatchMSData = o

        are_equal = (self.retention_times == other.retention_times).all()
        try:
            are_equal &= (self.retention_indices == other.retention_indices)
        except KeyError:
            pass
        are_equal &= self._spectra == other._spectra
        return are_equal

    @property
    def retention_times(self) -> Iterable[Data.RetentionTimeType]:
        """ Get retention times in seconds. """
        return self._retention_times.to('seconds')

    @property
    def retention_indices(self) -> Iterable[Data.RetentionIndexType]:
        """ Get retention indices. """
        return self._retention_indices

    @retention_indices.setter
    def retention_indices(self, values: Iterable[Data.RetentionIndexType]):
        """ Set retention indices. """
        if len(values) == len(self._spectra):
            self._retention_indices = values
            list(
                map(_assign_ri_value, self._spectra, [self._ri_key] * len(self._spectra), values)
            )
        else:
            raise ValueError('There is different numbers of computed indices and peaks.')


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


def _assign_ri_value(spectrum: Spectrum, key: str, value: Data.RetentionIndexType):
    """Assign RI value to Spectrum object

    Args:
        spectrum (Spectrum): Spectrum to add RI to
        value (Data.RetentionIndexType): RI to be added to Spectrum
    """
    if value is not None:
        retention_index = ('%f' % float(value)).rstrip('0').rstrip('.')
        spectrum.set(key=key, value=retention_index)
