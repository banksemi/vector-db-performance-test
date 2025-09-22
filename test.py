import numpy as np
import pandas as pd
from tqdm import tqdm
from src.databases.pgvector_database import PgVectorDatabase

pgvector = PgVectorDatabase()
pgvector.start(reset=False)

test_df = pd.read_parquet('datas/test.parquet')
neighbors_df = pd.read_parquet('datas/neighbors.parquet')

def recall(ground_truth_neighbors, predicted_neighbors):
    return len(set(ground_truth_neighbors).intersection(set(predicted_neighbors))) / len(ground_truth_neighbors)

for i in tqdm(range(len(test_df))):
    embedding = test_df.iloc[i]['emb']
    ground_truth_neighbors: np.ndarray = neighbors_df.iloc[i]['neighbors_id'][:10]
    predicted_neighbors = pgvector.get_neighbors(embedding, 10)

    recall_at_10 = recall(ground_truth_neighbors, predicted_neighbors)
    print(f"Recall@10: {recall_at_10}")