from abc import ABC, abstractmethod
from typing import Iterable, Optional, List
from pint import UnitRegistry
from pint.unit import build_unit_class


class Data(ABC):
    """ Base class for data managers. """
    RetentionTimeType = Optional[float]
    RetentionIndexType = Optional[float]
    URegistry = UnitRegistry()
    Unit = build_unit_class(URegistry)

    _rt_possible_keys = {'RT', 'rt', 'rts', 'retention_times', 'retention_time', 'retention', 'time', 'retentiontime'}
    _ri_possible_keys = {'RI', 'ri', 'ris', 'retention_indices', 'retention_index', 'kovats', 'retentionindex'}

    @staticmethod
    def is_valid(rt: RetentionTimeType) -> bool:
        return rt is not None and rt >= 0.0

    @classmethod
    def add_possible_rt_keys(cls, keys: List[str]):
        """ A method that adds new identifiers for the retention time information lookup. """
        cls._rt_possible_keys.update(keys)

    @classmethod
    def add_possible_ri_keys(cls, keys: List[str]):
        """ A method that adds new identifiers for the retention index information lookup. """
        cls._ri_possible_keys.update(keys)

    def __init__(self, filename: str, filetype: str, rt_unit: str):
        self._filename = filename
        self._filetype = filetype
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
    def retention_times(self) -> Iterable[RetentionTimeType]:
        ...

    @property
    @abstractmethod
    def retention_indices(self) -> Iterable[RetentionIndexType]:
        ...

    @retention_indices.setter
    @abstractmethod
    def retention_indices(self, value: Iterable[RetentionIndexType]):
        ...
