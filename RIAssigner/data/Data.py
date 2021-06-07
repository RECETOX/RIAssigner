from abc import ABC, abstractmethod
from typing import Iterable, Optional
from pint import Unit, UnitRegistry


class Data(ABC):
    """ Base class for data managers. """
    RetentionTimeType = Optional[float]
    RetentionIndexType = Optional[float]

    def __init__(self, filename: str, rt_unit: str = 'seconds'):
        self._filename = filename
        self._rt_unit = rt_unit
        self._unit = Unit(self._rt_unit)
        self._ureg = UnitRegistry()
        self.read()

    @abstractmethod
    def read(self):
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
