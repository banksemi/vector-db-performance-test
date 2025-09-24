from abc import ABC, abstractmethod

class FileDownloader(ABC):
    @abstractmethod
    def download_to_path(self, url: str) -> str:
        """
        파일 다운로드 후 Local Path를 반환합니다.
        :param url: 파일 URL
        :return: Local Path
        """