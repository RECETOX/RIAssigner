from abc import ABC, abstractmethod


class Data(ABC):
    """ Base class for data managers. """
    def __init__(self, filename: str):
        self._retention_times = []
        self._filename = filename
        self.read(self._filename)

    @abstractmethod
    def read(self, filename):
        ...

    @property
    def filename(self):
        return self._filename

    @property
    @abstractmethod
    def retention_times(self):
        ...

    @property
    @abstractmethod
    def retention_indices(self):
        ...
