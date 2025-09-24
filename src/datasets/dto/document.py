from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel

@dataclass
class Document:
    id: int
    embedding: NDArray[np.float64]
    field_1: int
    field_2: int
