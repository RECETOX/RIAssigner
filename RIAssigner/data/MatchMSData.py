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
        self._retention_times = []
        self._read_retention_times()

    def _read_spectra(self, filename):
        if filename.endswith('.msp'):
            self._spectra = list(load_from_msp(filename))
        else:
            raise NotImplementedError("Currently only supports 'msp'.")

    def _read_retention_times(self):
        for spectrum in self._spectra:
            rt = safe_read_rt(spectrum)
            self._retention_times.append(rt)

    @property
    def retention_times(self) -> Iterable[Optional[float]]:
        return self._retention_times

    @property
    def retention_indices(self) -> Iterable[Optional[int]]:
        raise NotImplementedError()

    @retention_indices.setter
    def retention_indices(self, values: Iterable[int]):
        if len(values) == len(self._spectra):
            for value_idx in range(len(values)):
                self._spectra[value_idx].set(key="retentionindex", value=values[value_idx])
        else:
            raise ValueError("There is different numbers of computed indices and peaks.")


def safe_read_rt(spectrum) -> Optional[float]:
    rt = spectrum.get('retentiontime', default=None)
    if rt is not None:
        try:
            rt = float(rt)
        except ValueError:
            # RT is in format that can't be converted to float -> set rt to None
            rt = None
    return rt


def _spectrum_has_rt(spectrum: Spectrum) -> bool:
    has_key = 'retentiontime' in spectrum.metadata.keys()
    if not has_key:
        return False
    return True
