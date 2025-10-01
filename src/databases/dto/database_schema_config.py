from typing import Optional

from pydantic import BaseModel

from src.databases.dto.indexes.interface import Index


class DatabaseSchemaConfig(BaseModel):
    index: Index
    reset_data: bool = False
    dim: Optional[int] = None
