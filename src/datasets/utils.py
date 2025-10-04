from typing import Iterator, Union

import pandas as pd
from tqdm import tqdm

from src.datasets.dto.answer_document import AnswerDocument
from src.datasets.dto.document import Document
from src.datasets.service.interface import Dataset


def make_dataframe_batch(df: pd.DataFrame, batch_size: int) -> Iterator[pd.DataFrame]:
    total = len(df)
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        datas = df.iloc[start:end]
        yield datas
