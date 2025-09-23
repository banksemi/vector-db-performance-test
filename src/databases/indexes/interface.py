from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.databases.indexes.distance import Distance


class Index(ABC, BaseModel):
    distance_metric: Distance