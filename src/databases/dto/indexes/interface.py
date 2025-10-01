from abc import ABC

from pydantic import BaseModel

from src.databases.dto.distance import Distance


class Index(ABC, BaseModel):
    distance_metric: Distance