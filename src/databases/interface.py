from abc import ABC, abstractmethod
from numpy.typing import NDArray
import numpy as np

class Database(ABC):
    @abstractmethod
    def start(self, reset=True):
        ...

    @abstractmethod
    def create_table(self, dim: int):
        ...

    @abstractmethod
    def insert_batch(self, idx: list[int], embedding: list[NDArray[np.float64]]):
        ...

    @abstractmethod
    def get_neighbors(self, embedding: NDArray[np.float64], limit: int) -> list[int]:
        ...

    @abstractmethod
    def close(self):
        ...
