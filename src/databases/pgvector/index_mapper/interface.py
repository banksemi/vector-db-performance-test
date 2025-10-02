from abc import ABC
from src.databases.dto.indexes.interface import Index
from src.databases.index_mapper import IndexMapper

class PGVectorIndexMapper[T: Index](IndexMapper[T, str], ABC):
    ...