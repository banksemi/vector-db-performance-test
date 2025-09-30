from abc import ABC, abstractmethod
from numpy.typing import NDArray
import numpy as np

from src.databases.indexes.interface import Index
from src.datasets.dto.answer_document import AnswerDocument
from src.datasets.dto.document import Document


class Database(ABC):
    @abstractmethod
    def start(self, reset=True):
        ...

    @abstractmethod
    def setup(self, dim: int, index: Index, reset_data=False):
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
