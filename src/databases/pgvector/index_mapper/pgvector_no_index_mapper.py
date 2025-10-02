from typing import Type

from src.databases.dto.indexes.interface import Index
from src.databases.dto.indexes.no_index import NoIndex
from src.databases.pgvector.index_mapper.interface import PGVectorIndexMapper


class PGVectorNoIndexMapper(PGVectorIndexMapper[NoIndex]):
   def convert_query(self, index: NoIndex) -> str:
      return ""
