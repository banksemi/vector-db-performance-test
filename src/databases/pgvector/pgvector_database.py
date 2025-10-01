import psycopg2
from psycopg2.extras import execute_values
import numpy as np

from src.databases.indexes.interface import Index
from src.databases.docker_based_database import DockerBasedDatabase
from src.databases.pgvector.index_mapper.interface import PGVectorIndexMapper
from src.datasets.dto.answer_document import AnswerDocument
from src.datasets.dto.document import Document


class PgVectorDatabase(DockerBasedDatabase):
    DOCKER_FOLDER = "docker/pgvector"

    def __init__(self, index_mappers: list[PGVectorIndexMapper]):
        super().__init__()

        self._index_mappers: dict[type[Index], PGVectorIndexMapper] = {}
        if index_mappers is not None:
            self._index_mappers = {
                mapper.get_input_class(): mapper for mapper in index_mappers
            }

        psycopg2.extensions.register_adapter(np.ndarray, lambda arr: psycopg2.extensions.adapt(arr.tolist()))

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
