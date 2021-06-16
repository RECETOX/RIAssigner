from abc import ABC, abstractmethod
from typing import Iterable, Optional
from pint import UnitRegistry
from pint.unit import build_unit_class


class Data(ABC):
    """ Base class for data managers. """
    RetentionTimeType = Optional[float]
    RetentionIndexType = Optional[float]
    URegistry = UnitRegistry()
    Unit = build_unit_class(URegistry)

    @staticmethod
    def is_valid(rt: RetentionTimeType) -> bool:
        return rt is not None and rt >= 0.0

    def __init__(self, filename: str, rt_unit: str = 'seconds'):
        self._filename = filename
        self._rt_unit = rt_unit
        self._unit = Data.Unit(self._rt_unit)
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
