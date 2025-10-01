from typing import Type

from src.databases.dto.indexes.hnsw_index import HNSWIndex
from src.databases.dto.indexes.interface import Index
from src.databases.opensearch.index_mapper.interface import OpenSearchIndexMapper
from src.databases.opensearch.space_type_mapper import get_space_type


class OpenSearchHNSWIndexMapper(OpenSearchIndexMapper):
    def get_input_class(self) -> Type[Index]:
        return HNSWIndex

    def convert_query(self, index: Index) -> dict:
        return {
            "name": "hnsw",
            "space_type": get_space_type(index.distance),
            "engine": "lucene"
        }
