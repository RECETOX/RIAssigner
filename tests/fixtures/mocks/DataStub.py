from typing import Iterable, Optional
from RIAssigner.data.Data import Data


class DataStub(Data):
    """ Mock class for data. """
    def __init__(self, retention_times: Iterable[float], retention_indices: Iterable[float]):
        self._retention_times = retention_times
        self._retention_indices = retention_indices
        self._retention_indices.sort()
        self._retention_times.sort()

    def read(self, filename):
        pass

    def write(self, filename):
        pass

    @property
    def filename(self):
        return "mock"

    @property
    def retention_times(self) -> Iterable[Optional[float]]:
        return self._retention_times

    @property
    def retention_indices(self) -> Iterable[Optional[float]]:
        return self._retention_indices

    @retention_indices.setter
    def retention_indices(self, value: Iterable[float]):
        self._retention_indices = value
