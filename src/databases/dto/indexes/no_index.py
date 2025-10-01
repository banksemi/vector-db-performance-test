from src.databases.dto.distance import Distance
from src.databases.dto.indexes.interface import Index


class NoIndex(Index):
    distance_metric: Distance = None
    ...