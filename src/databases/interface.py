from abc import ABC, abstractmethod

from src.databases.dto.database_schema_config import DatabaseSchemaConfig
from src.databases.dto.indexes.interface import Index
from src.datasets.dto.answer_document import AnswerDocument
from src.datasets.dto.document import Document


class Database(ABC):
    @abstractmethod
    def start(self, reset=True):
        ...

    @abstractmethod
    def setup(self, config: DatabaseSchemaConfig):
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
