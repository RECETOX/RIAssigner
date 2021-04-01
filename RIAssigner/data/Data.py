from abc import ABC, abstractmethod


class Data(ABC):
    """ Base class for data managers. """
    def __init__(self, filename: str):
        self._filename = filename

    @abstractmethod
    def read(self, filename):
        ...

    @property
    def filename(self):
        return self._filename
