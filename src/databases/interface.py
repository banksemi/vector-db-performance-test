from abc import ABC, abstractmethod
from numpy.typing import NDArray
import numpy as np

from src.databases.indexes.interface import Index
from src.datasets.dto.document import Document


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
    def insert_batch(self, documents: list[Document]):
        ...

    @abstractmethod
    def get_neighbors(self, document: AnswerDocument, limit: int) -> list[int]:
        ...

    @abstractmethod
    def close(self):
        ...

    @abstractmethod
    def set_ef_search(self, ef_search: int):
        ...
