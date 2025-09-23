from pydantic import BaseModel

from src.databases.indexes.distance import Distance
from src.databases.indexes.interface import Index


class HNSWIndex(Index):
    ...