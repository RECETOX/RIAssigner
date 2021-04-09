from abc import ABC, abstractmethod
from typing import List


class ComputationMethod(ABC):

    @abstractmethod
    def compute(query: Data, reference: Data) -> List[int]:
        ...