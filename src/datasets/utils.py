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


def tqdm_with_dataset(dataset: Dataset, mode='train', batch_size=100) -> Iterator[list[Union[Document, AnswerDocument]]]:
    if mode == 'train':
        pbar = tqdm(total=dataset.get_length_of_train())
        iter = dataset.get_train_datas(batch_size)
    elif mode == 'test':
        pbar = tqdm(total=dataset.get_length_of_test())
        iter = dataset.get_test_datas(batch_size)
    else:
        raise ValueError(f'Invalid mode: {mode}')

    for i in iter:
        pbar.update(len(i))
        yield i

