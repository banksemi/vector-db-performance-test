from typing import Iterator, Any

from tqdm import tqdm

from src.datasets.dto.answer_document import AnswerDocument
from src.datasets.dto.document import Document
from src.datasets.service.interface import Dataset


class DatasetTqdmMapper:
    def __init__(self, dataset: Dataset):
        self._dataset = dataset

    def get_train(self, batch_size: int = 100) -> Iterator[list[Document]]:
        pbar = tqdm(total=self._dataset.get_length_of_train())
        for i in self._dataset.get_train_datas(batch_size):
            pbar.update(len(i))
            yield i

    def get_test(self, batch_size: int = 100) -> Iterator[list[AnswerDocument]]:
        pbar = tqdm(total=self._dataset.get_length_of_test())
        for i in self._dataset.get_test_datas(batch_size):
            pbar.update(len(i))
            yield i
