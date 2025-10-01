from dishka import Provider, Scope

from src.file_downloader.file_download_impl import FileDownloaderImpl
from src.file_downloader.interface import FileDownloader


def get_provider() -> Provider:
    provider = Provider(scope=Scope.APP)
    provider.provide(FileDownloaderImpl, provides=FileDownloader)
    return provider
