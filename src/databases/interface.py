from abc import ABC, abstractmethod
from numpy.typing import NDArray
import numpy as np

from src.databases.indexes.interface import Index


class Database(ABC):
    @abstractmethod
    def start(self, reset=True):
        ...

    @abstractmethod
    def create_table(self, dim: int):
        ...

    @abstractmethod
    def create_index(self, index: Index):
        ...

    @abstractmethod
    def drop_index(self):
        ...

    @abstractmethod
    def insert_batch(self, idx: list[int], embedding: list[NDArray[np.float64]]):
        ...

    @abstractmethod
    def get_neighbors(self, embedding: NDArray[np.float64], limit: int, **kwargs) -> list[int]:
        ...

    @abstractmethod
    def close(self):
        ...

    @abstractmethod
    def set_ef_search(self, ef_search: int):
        ...
