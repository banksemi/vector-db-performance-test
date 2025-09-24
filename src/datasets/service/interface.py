from abc import ABC, abstractmethod
from typing import Iterator

from src.datasets.dto.answer_document import AnswerDocument
from src.datasets.dto.document import Document


class Dataset(ABC):
    @abstractmethod
    def get_vector_size(self):
        ...

    @abstractmethod
    def get_length_of_train(self) -> int:
        ...

    @abstractmethod
    def get_length_of_test(self) -> int:
        ...

    @abstractmethod
    def get_train_datas(self, batch_size: int) -> Iterator[list[Document]]:
        ...

    @abstractmethod
    def get_test_datas(self, batch_size: int) -> Iterator[list[AnswerDocument]]:
        ...
