from opensearchpy import OpenSearch, helpers

from src.databases.docker_based_database import DockerBasedDatabase
from src.databases.dto.database_schema_config import DatabaseSchemaConfig
from src.databases.opensearch.index_mapper.interface import OpenSearchIndexMapper

from src.datasets.dto.answer_document import AnswerDocument
from src.datasets.dto.document import Document

class OpenSearchDatabase(DockerBasedDatabase):
    DOCKER_FOLDER = "docker/opensearch"
    def __init__(self, index_mappers: list[OpenSearchIndexMapper]):
        super().__init__()
        self.dim: int | None = None
        self._index_name = 'index1'
        self._index_mappers = {
            mapper.get_input_class(): mapper for mapper in index_mappers
        }


    def start(self, reset=True):
        super().start(reset=reset)
        self._client = OpenSearch(
            hosts=[{'host': 'localhost', 'port': 9200}],
            timeout=60,
            max_retries=3,
            retry_on_timeout=True
        )

    def setup(self, config: DatabaseSchemaConfig):
        if config.dim is not None:
            self.dim = config.dim

        if config.reset_data == False:
            raise Exception("OpenSearch cannot change the index while keeping the data. Please enable reset_data.")
        if self.dim is None:
            raise Exception("dim is not defined")

        self._client.indices.delete(index=self._index_name, ignore=[404])
        index_type = type(config.index)

        if index_type not in self._index_mappers:
            raise Exception("Not supported index")

        embedding_field = {
            "type": "knn_vector",
            "dimension": self.dim,
        }

        method: dict = self._index_mappers[index_type].convert_query(config.index)
        if method:
            embedding_field["method"] = method

        mapping = {
            "mappings": {
                "properties": {
                    'field_1': {'type': 'integer'},
                    'embedding': embedding_field,
                }
            },
            "settings": {
                "index": {
                    "knn": True,
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                }
            }
        }

        self._client.indices.create(index=self._index_name, body=mapping)

    def insert_batch(self, documents: list[Document]):
        batch = []
        for document in documents:
            batch.append({
                '_id': document.id,
                '_source': {
                    'field_1': document.field_1,
                    'field_2': document.field_2,
                    'embedding': document.embedding,
                },
                '_index': self._index_name
            })
        response = helpers.bulk(self._client, batch)

    def get_neighbors(self, document: AnswerDocument, limit: int) -> list[int]:
        query = {
            "_source": False, # 문서 원본은 필요하지 않음 (_id만 필요)
            "size": limit,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": document.embedding,
                        "k": limit
                    }
                }
            }
        }

        response = self._client.search(index=self._index_name, body=query)
        return [int(hit['_id']) for hit in response['hits']['hits']]

    def set_ef_search(self, ef_search: int):
        raise NotImplementedError()