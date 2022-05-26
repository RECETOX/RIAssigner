from abc import ABC, abstractmethod
from typing import Iterable, List, Optional

from pint import Quantity, UnitRegistry
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
        """Determine whether a retention time value is valid

        Args:
            rt (RetentionTimeType): Value to check for validity.

        Returns:
            bool: State of validity (True/False).
        """
        result = rt is not None and Data.can_be_float(rt) and rt >= 0.0
        return result

    @staticmethod
    def can_be_float(rt):
        if isinstance(rt, (Quantity, float, int)):
            return True
        return False

    @classmethod
    def add_possible_rt_keys(cls, keys: List[str]):
        """ A method that adds new identifiers for the retention time information lookup. """
        cls._rt_possible_keys.update(keys)

    @classmethod
    def add_possible_ri_keys(cls, keys: List[str]):
        """ A method that adds new identifiers for the retention index information lookup. """
        cls._ri_possible_keys.update(keys)

    @classmethod
    def get_possible_rt_keys(cls) -> List[str]:
        """Method to get the supported retention time keys

        Returns:
            List[str]: List of supported retention time keys.
        """
        return cls._rt_possible_keys.copy()

    @classmethod
    def get_possible_ri_keys(cls) -> List[str]:
        """Method to get the supported retention index keys

        Returns:
            List[str]: List of supported retention index keys.
        """
        return cls._ri_possible_keys.copy()

    def __init__(self, filename: str, filetype: str, rt_unit: str):
        self._filename = filename
        self._filetype = filetype
        self._rt_unit = rt_unit
        self._unit = Data.Unit(self._rt_unit)

    @abstractmethod
    def write(self, filename):
        """Store current content to disk.

        Args:
            filename (str): Path to output filename.
        """
        ...

    @property
    def filename(self) -> str:
        """Getter for filename property.

        Returns:
            str: Filename of originally loaded data.
        """
        return self._filename

    @property
    @abstractmethod
    def retention_times(self) -> Iterable[RetentionTimeType]:
        """Getter for `retention_times` property.

        Returns:
            Iterable[RetentionTimeType]: RT values contained in data.
        """
        ...

    @property
    @abstractmethod
    def retention_indices(self) -> Iterable[RetentionIndexType]:
        """Getter for `retention_indices` property.

        Returns:
            Iterable[RetentionIndexType]: RI values stored in data.
        """
        ...

    @retention_indices.setter
    @abstractmethod
    def retention_indices(self, value: Iterable[RetentionIndexType]):
        """Setter for `retention_indices` variable.

        Args:
            value (Iterable[RetentionIndexType]): Values to assign to property.
        """
        ...
