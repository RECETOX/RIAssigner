from typing import Iterable, List, Optional, Tuple
import numpy as np

from matchms import Spectrum, Metadata
from matchms.exporting import save_spectra
from matchms.exporting.metadata_export import get_metadata_as_array
from matchms.importing import load_spectra

from .Data import Data


class MatchMSData(Data):
    """ Class to handle data from filetypes which can be imported
        using 'matchms'.
    """

    def __init__(self, filename: str, filetype: str, rt_unit: str):
        super().__init__(filename, filetype, rt_unit)
        self._read()

    def _read(self):
        """Load data into object and initialize properties.
        """
        self._spectra = list(load_spectra(self._filename, True, self._filetype))
        _, self._keys = get_metadata_as_array(self._spectra)
        
        self._rt_key = "retention_time"
        self._ri_key = "retention_index"

        self._sort_spectra_by_rt()

        self._read_retention_times()
        self._read_retention_indices()

    def write(self, filename: str) -> None:
        """Write data to back to the spectra file

        Args:
            filename (str): Path to filename under which to store the data.
        """
        self._write_RIs_to_spectra()
        save_spectra(self._spectra, filename)

    def _write_RIs_to_spectra(self)  -> None:
        """Write the RI values stored in the object to the spectra metadata.
        """
        list(map(_assign_ri_value, self._spectra, [self._ri_key] * len(self._spectra), self._retention_indices))

    def _read_retention_times(self) -> None:
        """ Read retention times from spectrum metadata. """
        magnitude = [safe_read_key(spectrum, self._rt_key) for spectrum in self._spectra]
        self._retention_times = Data.URegistry.Quantity(magnitude, self._unit)

    def _read_retention_indices(self) -> None:
        """ Read retention indices from spectrum metadata. """
        self.retention_indices = [safe_read_key(spectrum, self._ri_key) for spectrum in self._spectra]

    def _sort_spectra_by_rt(self) -> None:
        """ Sort objects (peaks) in spectra list by their retention times. """
        self._spectra.sort(key=lambda spectrum: safe_read_key(spectrum, self._rt_key) or 0)

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
        else:
            raise ValueError('There is different numbers of computed indices and peaks.')

    @property
    def comment(self) -> Iterable[Data.CommentFieldType]:
        """ Get comments."""
        self.comment_keys = "comment"
        content = [spectrum.get(self.comment_keys, default=None) for spectrum in self._spectra]
        return content

    @property
    def spectra_metadata(self) -> Tuple[np.array, List[str]]:
        return get_metadata_as_array(self._spectra)
    
def safe_read_key(spectrum: Spectrum, key: str) -> float:
    """ Read key from spectrum and convert to float or return 0.0.
    Tries to read the given key from the spectrum metadata and convert it to a float.
    In case an exception is thrown or the key is not present, returns 0.0.

    Parameters
    ----------
    spectrum:
        Spectrum from which to read the key.
    key:
        Key to be read from the spectrum metadata.

    Returns
    -------
        Either the key's value converted to float or 0.0.
    """

    value = spectrum.get(key, default=0.0)
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            # RT is in format that can't be converted to float -> set rt to 0.0
            value = 0.0
    if not Data.can_be_float(value):
        value = 0.0
    return value

def _assign_ri_value(spectrum: Spectrum, key: str, value: Data.RetentionIndexType) -> None:
    """Assign RI value to Spectrum object

    Args:
        spectrum (Spectrum): Spectrum to add RI to
        value (Data.RetentionIndexType): RI to be added to Spectrum
    """
    if value > 0:
        retention_index = ('%f' % float(value)).rstrip('0').rstrip('.')
        spectrum.set(key=key, value=retention_index)
    else:
        if spectrum.get(key):
            metadata = spectrum.metadata
            del metadata[key]
            spectrum.metadata = metadata
        
