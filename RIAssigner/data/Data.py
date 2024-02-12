from abc import ABC, abstractmethod
from typing import Iterable, List, Optional, Union
import pandas as pd

from pint import Quantity, UnitRegistry
from matchms.utils import load_known_key_conversions


class Data(ABC):
    """ Base class for data managers. """
    RetentionTimeType = float
    RetentionIndexType = float
    CommentFieldType = Optional[str]
    URegistry = UnitRegistry()
    _keys_conversions = load_known_key_conversions()
    _rt_possible_keys = [ key for key , value in _keys_conversions.items() if "retention_time" == value] + ["retention_time"]
    _ri_possible_keys = [ key for key , value in _keys_conversions.items() if "retention_index" == value] + ["retention_index"]

    @staticmethod
    def is_valid(value: Union[RetentionTimeType, RetentionIndexType]) -> bool:
        """Determine whether a retention time value is valid

        Args:
            rt (RetentionTimeType): Value to check for validity.

        Returns:
            bool: State of validity (True/False).
        """
        result = value is not None and Data.can_be_float(value) and value > 0
        return result

    @staticmethod
    def can_be_float(rt: Union[Quantity, float, int]) -> bool:
        """Determine whether a value can be converted to a float.

        This function checks if the provided input is an instance of either
        Quantity, float, or int.

        Args:
            rt (Union[Quantity, float, int]): Value to check for float conversion.

        Returns:
            bool: True if the input is an instance of Quantity, float, or int, False otherwise.
        """
        if isinstance(rt, (Quantity, float, int)):
            return True
        return False

    @classmethod
    def add_possible_rt_keys(cls, keys: List[str]) -> None:
        """ A method that adds new identifiers to get retention time information.

        Args:
            keys (List[str]): A list of new identifiers (keys) to be added to the `_rt_possible_keys`.

        Returns:
            None
        """
        cls._rt_possible_keys.append(keys)

    @classmethod
    def add_possible_ri_keys(cls, keys: List[str]) -> None:
        """ A method that adds new identifiers to get retention index information. 

        Args:
            keys (List[str]): A list of new identifiers (keys) to be added to the `_ri_possible_keys`.

        Returns:
            None
        """
        cls._ri_possible_keys.append(keys)
    
    @classmethod
    def get_possible_rt_keys(cls) -> List[str]:
        """ A method that returns the possible keys to get retention times.
        
        Returns:
            List[str]:  A list of possible keys to get retention times.
        """
        return cls._rt_possible_keys
    
    @classmethod
    def get_possible_ri_keys(cls) -> List[str]:
        """ A method that returns the possible keys to get retention indices.

        Returns:
            List[str]:  A list of possible keys to get retention indices.
        """
        return cls._ri_possible_keys

    def __init__(self, filename: str, filetype: str, rt_unit: str):
        self._filename = filename
        self._filetype = filetype
        self._rt_unit = rt_unit
        self._unit = Data.URegistry(self._rt_unit)

    @abstractmethod
    def write(self, filename: str) -> None:
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
    def retention_indices(self, value: Iterable[RetentionIndexType]) -> None:
        """Setter for `retention_indices` variable.

        Args:
            value (Iterable[RetentionIndexType]): Values to assign to property.
        """
        ...

    def has_retention_indices(self) -> bool:
        """
        Check if all retention indices in the spectra exist.

        This method iterates over the retention indices in the spectra. If it encounters a value that is None,
        it immediately returns False. If it iterates over all retention indices without finding a None value,
        it returns True.

        Returns:
            bool: True if all retention indices exist, False otherwise.
        """
        return len(self.retention_indices) > 0 and all([Data.is_valid(rt) for rt in self.retention_indices])
    
    def has_retention_times(self) -> bool:
        """
        Check if all retention times in the spectra exist.

        This method iterates over the retention times in the spectra. If it encounters a value that is None,
        it immediately returns False. If it iterates over all retention times without finding a None value,
        it returns True.

        Returns:
            bool: True if all retention times exist, False otherwise.
        """
        return len(self.retention_times) > 0 and all([Data.is_valid(rt) for rt in self.retention_times])


    @property
    @abstractmethod
    def comment(self) -> Iterable[CommentFieldType]:
        """Getter for `comment` property.

        Returns:
            Iterable[CommentFieldType]: Comment field values stored in data.
        """
        ...

    def init_ri_from_comment(self, ri_source: str) -> None:
        """ Extract RI from comment field.
        Extracts the RI from the comment field of the data file. The RI is expected to be
        in the format 'ri_source=RI_value'. The function extracts the RI value and
        sets it on the retention_index property.

        Parameters
        ----------
        content_comment:
            Comment field of the data file. 
        ri_source:
            String that is expected to be in the comment field before the RI value.
        """
        mask = pd.Series(self.comment).str.contains(rf'\b{ri_source}\b', na=False)
        extracted_values = pd.Series(self.comment).str.extract(rf'\b{ri_source}=(\d+)\b')[0].astype(float)
        self.retention_indices = extracted_values.where(mask, None).tolist()
        
