from src.databases.docker_based_database import DockerBasedDatabase
import psycopg2
from psycopg2.extras import execute_values

import numpy as np
from numpy.typing import NDArray

def adapt_numpy_array(arr):
    return psycopg2.extensions.adapt(arr.tolist())

class PgVectorDatabase(DockerBasedDatabase):
    COMPOSE_FILE = "docker/pgvector.yaml"

    def start(self, reset=True):
        super().start(reset=reset)
        psycopg2.extensions.register_adapter(np.ndarray, adapt_numpy_array)
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

    def get_neighbors(self, embedding: NDArray[np.float64], limit: int) -> list[int]:
        with self._conn.cursor() as cur:
            cur.execute(f"""
                        WITH q AS (SELECT %s::vector AS qvec)
                        SELECT idx, 1 - (emb <=> qvec) AS cosine_similarity
                        FROM items,
                             q
                        ORDER BY cosine_similarity DESC LIMIT {limit};
                        """, (embedding,))
            rows = cur.fetchall()
            return [i[0] for i in rows]

    def close(self):
        self._conn.close()
        super().close()

