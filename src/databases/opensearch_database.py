from src.databases.docker_based_database import DockerBasedDatabase
from src.databases.indexes.distance import Distance
from src.databases.indexes.hnsw_index import HNSWIndex
from src.databases.indexes.interface import Index
from src.datasets.dto.answer_document import AnswerDocument
from src.datasets.dto.document import Document
from opensearchpy import OpenSearch

class OpenSearchDatabase(DockerBasedDatabase):
    DOCKER_FOLDER = "docker/opensearch"
    def __init__(self):
        super().__init__()
        self.dim = None

    def start(self, reset=True):
        super().start(reset=reset)
        self._client = OpenSearch(
            hosts=[{'host': 'localhost', 'port': 9200}],
            timeout=60,
            max_retries=3,
            retry_on_timeout=True
        )

    def create_table(self, dim: int):
        self.dim = dim

    def create_index(self, index: Index):
        if self.dim is None:
            raise Exception("dim is not defined")
        if not isinstance(index, HNSWIndex):
            raise Exception("Not supported index")

        space_type = None
        if index.distance_metric == Distance.COSINE:
            space_type = "cosinesimil"
        else:
            raise Exception("Not supported distance metric")

        mapping = {
            "mappings": {
                "properties": {
                    'field_1': {'type': 'integer'},
                    'embedding': {
                        "type": "knn_vector",
                        "dimension": self.dim,
                        "method": {
                            "name": "hnsw",
                            "space_type": space_type,
                            "engine": "lucene"
                        }
                    },
                }
            },
            "settings": {
                "index": {
                    "knn": True,
                    "knn.algo_param.ef_search": 100,
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                }
            }
        }

        self._client.indices.create(index='index1', body=mapping)

    def drop_index(self):
        pass

    def insert_batch(self, documents: list[Document]):
        pass

    def get_neighbors(self, document: AnswerDocument, limit: int) -> list[int]:
        pass

    def set_ef_search(self, ef_search: int):
        pass
