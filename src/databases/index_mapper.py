from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic, get_args, get_origin
from types import get_original_bases

from src.databases.dto.indexes.interface import Index


class IndexMapper[T: Index, RT](ABC):
    @abstractmethod
    def convert_query(self, index: T) -> RT:
        ...

    def get_input_class(self) -> Type[T]:
        return self._get_entity_type()[0]

    @classmethod
    def _get_entity_type(cls) -> tuple[Type[T], ...]:
        for generic_base in get_original_bases(cls):
            if issubclass(get_origin(generic_base), IndexMapper):
                return get_args(generic_base)

        raise RuntimeError("IndexMapper가 상속되었지만, 탐색할 수 없음 [모순]")
