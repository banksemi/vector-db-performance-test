from src.databases.indexes.distance import Distance
from src.databases.indexes.interface import Index


class NoIndex(Index):
    distance_metric: Distance = None
    ...