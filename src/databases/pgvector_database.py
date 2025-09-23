from src.databases.docker_based_database import DockerBasedDatabase
import psycopg2
from psycopg2.extras import execute_values
import numpy as np
from numpy.typing import NDArray

from src.databases.indexes.distance import Distance
from src.databases.indexes.hnsw_index import HNSWIndex
from src.databases.indexes.interface import Index

def adapt_numpy_array(arr):
    return psycopg2.extensions.adapt(arr.tolist())
psycopg2.extensions.register_adapter(np.ndarray, adapt_numpy_array)

class PgVectorDatabase(DockerBasedDatabase):
    COMPOSE_FILE = "docker/pgvector.yaml"

    def start(self, reset=True):
        super().start(reset=reset)
        self._conn = psycopg2.connect(
            host="localhost",
            port="5432",
            dbname="vectordb",
            user="postgres",
            password="postgres"
        )

    def create_table(self, dim: int):
        with self._conn.cursor() as cur:
            cur.execute(f"""
                   CREATE EXTENSION IF NOT EXISTS vector;
                   CREATE TABLE items (
                        idx INTEGER PRIMARY KEY,
                     emb VECTOR({dim})
                 );
            """)

    def insert_batch(self, idx: list[int], embedding: list[NDArray[np.float64]]):
        with self._conn.cursor() as cur:
            rows = list(zip(idx, embedding))
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

    def get_neighbors(self, embedding: NDArray[np.float64], limit: int, **kwargs) -> list[int]:
        with self._conn.cursor() as cur:
            vector_str = '[' +  ','.join(map(str, embedding)) + ']'

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

    def create_index(self, index: Index):
        if isinstance(index, HNSWIndex):
            with self._conn.cursor() as cur:
                distance_metric = None
                if index.distance_metric == Distance.COSINE:
                    distance_metric = "vector_cosine_ops"
                else:
                    raise Exception("Not supported distance metric")
                cur.execute(f"""
                    CREATE INDEX index1
                    ON items USING hnsw (emb {distance_metric})
                """)
                self._conn.commit()

        else:
            raise Exception("Not supported index")

    def drop_index(self):
        with self._conn.cursor() as cur:
            cur.execute("DROP INDEX IF EXISTS index1")
            self._conn.commit()
