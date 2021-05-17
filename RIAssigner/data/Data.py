from abc import ABC, abstractmethod
from typing import Iterable, Optional


class Data(ABC):
    """ Base class for data managers. """
    RetentionTimeType = Optional[float]
    RetentionIndexType = Optional[float]

    @staticmethod
    def is_valid(rt: RetentionTimeType) -> bool:
        return rt is not None and rt >= 0.0

    def __init__(self, filename: str):
        self._filename = filename
        self.read(self._filename)

    @abstractmethod
    def read(self, filename):
        ...

    @abstractmethod
    def write(self, filename):
        ...

    @property
    def filename(self):
        return self._filename

    @property
    @abstractmethod
    def retention_times(self) -> Iterable[Optional[float]]:
        ...

    @property
    @abstractmethod
    def retention_indices(self) -> Iterable[Optional[float]]:
        ...

    @retention_indices.setter
    @abstractmethod
    def retention_indices(self, value: Iterable[float]):
        ...
