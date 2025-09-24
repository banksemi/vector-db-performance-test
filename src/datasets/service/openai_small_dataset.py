from typing import Iterator

from src.datasets.dto.answer_document import AnswerDocument
from src.datasets.dto.document import Document
from src.datasets.service.interface import Dataset
import requests
import os
from tqdm import tqdm
import pandas as pd

from src.datasets.utils import make_dataframe_batch
from src.file_downloader.interface import FileDownloader


class OpenAISmallDataset(Dataset):
    def __init__(self, file_downloader: FileDownloader):
        self._file_downloader = file_downloader
        self._base_url = "https://assets.zilliz.com/benchmark/openai_small_50k/"

        self._train_df = self._download('train.parquet')
        self._test_df = self._download('test.parquet')
        self._neighbors_df = self._download('neighbors.parquet')

    def _download(self, file_name) -> pd.DataFrame:
        url = self._base_url + file_name
        local_path = self._file_downloader.download_to_path(url)
        return pd.read_parquet(local_path)

    def get_vector_size(self):
        return 1536

    def get_test_datas(self, batch_size: int) -> Iterator[list[AnswerDocument]]:
        for test_df, neighbor_df in zip(
                make_dataframe_batch(self._test_df, batch_size),
                make_dataframe_batch(self._neighbors_df, batch_size)
        ):
            result = []
            for embedding, neighbors in zip(test_df['emb'].tolist(), neighbor_df['neighbors_id'].tolist()):
                result.append(AnswerDocument(embedding=embedding, neighbors=neighbors))
            yield result

    def get_train_datas(self, batch_size: int) -> Iterator[list[Document]]:
        for df in make_dataframe_batch(self._train_df, batch_size):
            result = []
            for idx, embedding in zip(df['id'].tolist(), df['emb'].tolist()):
                result.append(Document(id=idx, embedding=embedding, field_1=0, field_2=0))
            yield result

    def get_length_of_test(self) -> int:
        return len(self._test_df)

    def get_length_of_train(self) -> int:
        return len(self._train_df)