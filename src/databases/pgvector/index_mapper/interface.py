from abc import ABC, abstractmethod
from typing import Type

from src.databases.dto.indexes.interface import Index


class PGVectorIndexMapper(ABC):
    @abstractmethod
    def get_input_class(self) -> Type[Index]:
        ...

    @abstractmethod
    def convert_query(self, index: Index) -> str:
        ...