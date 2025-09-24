from dataclasses import dataclass
from typing import Optional

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel

@dataclass
class AnswerDocument:
    embedding: NDArray[np.float64]
    neighbors: list[int]
    field_1: Optional[int] = None
    field_2: Optional[int] = None