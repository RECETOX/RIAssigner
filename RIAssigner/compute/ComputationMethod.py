from abc import ABC, abstractmethod
from typing import List
from RIAssigner.data import Data


class ComputationMethod(ABC):

    @abstractmethod
    def compute(self, query: Data, reference: Data) -> List[float]:
        ...
