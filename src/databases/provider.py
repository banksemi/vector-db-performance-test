from dishka import Provider, Scope

from src.databases.opensearch.index_mapper.interface import OpenSearchIndexMapper
from src.databases.opensearch.index_mapper.opensearch_hnsw_index_mapper import OpenSearchHNSWIndexMapper
from src.databases.opensearch.index_mapper.opensearch_no_index_mapper import OpenSearchNoIndexMapper
from src.databases.opensearch.opensearch_database import OpenSearchDatabase
from src.databases.pgvector.index_mapper.interface import PGVectorIndexMapper
from src.databases.pgvector.index_mapper.pgvector_hnsw_index_mapper import PGVectorHNSWIndexMapper
from src.databases.pgvector.index_mapper.pgvector_no_index_mapper import PGVectorNoIndexMapper
from src.databases.pgvector.pgvector_database import PgVectorDatabase


def get_provider() -> Provider:
    provider = Provider(scope=Scope.APP)
    provider.provide(PGVectorHNSWIndexMapper, provides=PGVectorIndexMapper)
    provider.provide(PGVectorNoIndexMapper, provides=PGVectorIndexMapper)
    provider.provide(PgVectorDatabase)

    provider.provide(OpenSearchDatabase)
    provider.provide(OpenSearchNoIndexMapper, provides=OpenSearchIndexMapper)
    provider.provide(OpenSearchHNSWIndexMapper, provides=OpenSearchIndexMapper)
    return provider
