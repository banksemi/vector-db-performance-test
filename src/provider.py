from dishka import make_container, Container

from src.container_utils import get_list_provider
from src.databases.provider import get_provider as get_database_provider
from src.file_downloader.provider import get_provider as get_file_downloader_provider
from src.datasets.provider import get_provider as get_dataset_provider

def get_container() -> Container:
    providers = [
        get_database_provider(),
        get_file_downloader_provider(),
        get_dataset_provider(),
    ]

    list_providers = get_list_provider(*providers)
    return make_container(*providers, list_providers)
