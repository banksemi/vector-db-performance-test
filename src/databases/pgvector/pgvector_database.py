from typing import Optional

from src.databases.docker_based_database import DockerBasedDatabase
import psycopg2
from psycopg2.extras import execute_values
import numpy as np
from numpy.typing import NDArray

from src.databases.indexes.distance import Distance
from src.databases.indexes.no_index import NoIndex
from src.databases.indexes.hnsw_index import HNSWIndex
from src.databases.indexes.interface import Index
from src.databases.pgvector.index_mapper.interface import PGVectorIndexMapper
from src.datasets.dto.answer_document import AnswerDocument
from src.datasets.dto.document import Document


def adapt_numpy_array(arr):
    return psycopg2.extensions.adapt(arr.tolist())
psycopg2.extensions.register_adapter(np.ndarray, adapt_numpy_array)

class PgVectorDatabase(DockerBasedDatabase):
    DOCKER_FOLDER = "docker/pgvector"

    def __init__(self, index_mappers: Optional[list[PGVectorIndexMapper]] = None):
        # 주의: index_mappers의 기본 값으로 [] 을 사용하면 의도치 않게 기본 값을 수정할 수 있어 사이드 이펙트 발생 가능

        super().__init__()

        self._index_mappers: dict[type[Index], PGVectorIndexMapper] = {}
        if index_mappers is not None:
            self._index_mappers = {
                mapper.get_input_class(): mapper for mapper in index_mappers
            }

    def start(self, reset=True):
        super().start(reset=reset)
        self._conn = psycopg2.connect(
            host="localhost",
            port="5432",
            dbname=self.get_env_value("POSTGRES_DB"),
            user=self.get_env_value("POSTGRES_USER"),
            password=self.get_env_value("POSTGRES_PASSWORD")
        )
        with self._conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

    def setup(self, dim: int, index: Index, reset_data=False):
        with self._conn.cursor() as cur:
            if reset_data:
                cur.execute("DROP TABLE IF EXISTS items")

            cur.execute(f"""
                   CREATE TABLE IF NOT EXISTS items (
                        idx INTEGER PRIMARY KEY,
                        emb VECTOR({dim})
                 );
            """)

            self._create_index(index)

    def insert_batch(self, documents: list[Document]):
        with self._conn.cursor() as cur:
            rows = [(i.id, i.embedding) for i in documents]
            execute_values(
                cur,
                "INSERT INTO items (idx, emb) VALUES %s",
                rows,
                # page_size=1000
            )
            self._conn.commit()

    def set_ef_search(self, ef_search: int):
        with self._conn.cursor() as cur:
            cur.execute(f"SET hnsw.ef_search = {ef_search}")
            self._conn.commit()

    def get_neighbors(self, document: AnswerDocument, limit: int) -> list[int]:
        with self._conn.cursor() as cur:
            vector_str = '[' +  ','.join(map(str, document.embedding)) + ']'

            cur.execute(f"""
                        SELECT idx
                        FROM items
                        ORDER BY (emb <=> %s) LIMIT %s;
                        """, (vector_str,limit))
            rows = cur.fetchall()
            return [i[0] for i in rows]

    def close(self):
        self._conn.close()
        super().close()

    def _create_index(self, index: Index):
        with self._conn.cursor() as cur:
            cur.execute("DROP INDEX IF EXISTS index1")

            index_class = type(index)
            if index_class not in self._index_mappers:
                raise Exception("Not supported index")

            query: str = self._index_mappers[index_class].convert_query(index)
            if query:
                cur.execute(query)
                self._conn.commit()
