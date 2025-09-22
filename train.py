import pandas as pd
from tqdm import tqdm
from src.databases.pgvector_database import PgVectorDatabase

pgvector = PgVectorDatabase()
pgvector.start(reset=True)

train_df = pd.read_parquet('datas/train.parquet')
test_df = pd.read_parquet('datas/test.parquet')
neighbors_df = pd.read_parquet('datas/neighbors.parquet')


vector_size = len(train_df.iloc[0]['emb'])

pgvector.create_table(vector_size)

batch_size = 100
total = len(train_df)
i = 0
for start in tqdm(range(0, total, batch_size)):
    end = min(start + batch_size, total)
    datas = train_df.iloc[start:end]
    pgvector.insert_batch(
        idx=datas['id'].tolist(),
        embedding=datas['emb'].tolist()
    )