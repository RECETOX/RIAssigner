from abc import ABC, abstractmethod
from RIAssigner.data import Data
from typing import List



class ComputationMethod(ABC):

    @abstractmethod
    def compute(query: Data, reference: Data) -> List[int]:
        ...
