from typing import Optional
from src.databases.indexes.interface import Index


class HNSWIndex(Index):
    ef_construction: Optional[int] = None
    m: Optional[int] = None
