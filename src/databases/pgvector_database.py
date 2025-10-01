from src.databases.docker_based_database import DockerBasedDatabase
import psycopg2
from psycopg2.extras import execute_values
import numpy as np
from numpy.typing import NDArray

from src.databases.indexes.distance import Distance
from src.databases.indexes.empty_index import EmptyIndex
from src.databases.indexes.hnsw_index import HNSWIndex
from src.databases.indexes.interface import Index
from src.datasets.dto.answer_document import AnswerDocument
from src.datasets.dto.document import Document


def adapt_numpy_array(arr):
    return psycopg2.extensions.adapt(arr.tolist())
psycopg2.extensions.register_adapter(np.ndarray, adapt_numpy_array)

class PgVectorDatabase(DockerBasedDatabase):
    DOCKER_FOLDER = "docker/pgvector"

    def start(self, reset=True):
        super().start(reset=reset)
        self._conn = psycopg2.connect(
            host="localhost",
            port="5432",
            dbname=self.get_env_value("POSTGRES_DB"),
            user=self.get_env_value("POSTGRES_USER"),
            password=self.get_env_value("POSTGRES_PASSWORD")
        )

    def setup(self, dim: int, index: Index, reset_data=False):
        with self._conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            cur.execute("DROP INDEX IF EXISTS index1")
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
        if isinstance(index, EmptyIndex):
            return

        if isinstance(index, HNSWIndex):
            with self._conn.cursor() as cur:
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
                cur.execute(query)
                self._conn.commit()

        else:
            raise Exception("Not supported index")