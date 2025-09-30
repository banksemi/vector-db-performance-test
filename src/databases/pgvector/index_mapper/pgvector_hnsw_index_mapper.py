from typing import Type

from src.databases.indexes.distance import Distance
from src.databases.indexes.hnsw_index import HNSWIndex
from src.databases.indexes.interface import Index
from src.databases.pgvector.index_mapper.interface import PGVectorIndexMapper


class PGVectorHNSWIndexMapper(PGVectorIndexMapper):
    def get_input_class(self) -> Type[Index]:
        return HNSWIndex

    def convert_query(self, index: Index) -> str:
        distance_metric = None

        if index.distance_metric == Distance.COSINE:
            distance_metric = "vector_cosine_ops"
        else:
            raise Exception("Not supported distance metric")

        options = {}
        if index.ef_construction is not None:
            options['ef_construction'] = index.ef_construction

        if index.m is not None:
            options['m'] = index.m

        query = f"CREATE INDEX index1 ON items USING hnsw (emb {distance_metric})"
        if len(options) > 0:
            query_strs = []
            for key, value in options.items():
                query_strs.append(f"{key}={value}")
            query += f" WITH ({', '.join(query_strs)})"
        return query
