from dishka import Provider, Scope

from src.databases.pgvector.index_mapper.interface import PGVectorIndexMapper
from src.databases.pgvector.index_mapper.pgvector_hnsw_index_mapper import PGVectorHNSWIndexMapper
from src.databases.pgvector.index_mapper.pgvector_no_index_mapper import PGVectorNoIndexMapper
from src.databases.pgvector.pgvector_database import PgVectorDatabase


def get_provider() -> Provider:
    provider = Provider(scope=Scope.APP)
    provider.provide(PGVectorHNSWIndexMapper, provides=PGVectorIndexMapper)
    provider.provide(PGVectorNoIndexMapper, provides=PGVectorIndexMapper)
    provider.provide(PgVectorDatabase)
    return provider
