from typing import Type

from src.databases.dto.indexes.interface import Index
from src.databases.dto.indexes.no_index import NoIndex
from src.databases.pgvector.index_mapper.interface import PGVectorIndexMapper


class PGVectorNoIndexMapper(PGVectorIndexMapper):
    def get_input_class(self) -> Type[Index]:
        return NoIndex

    def convert_query(self, index: Index) -> str:
        return ""
