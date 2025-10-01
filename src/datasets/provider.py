from dishka import Provider, Scope

from src.datasets.service.openai_small_dataset import OpenAISmallDataset


def get_provider() -> Provider:
    provider = Provider(scope=Scope.APP)
    provider.provide(OpenAISmallDataset)
    return provider
