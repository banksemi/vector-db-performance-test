from abc import ABC, abstractmethod

from python_on_whales import DockerClient
from src.databases.interface import Database


class DockerBasedDatabase(Database, ABC):
    COMPOSE_FILE = None

    def __init__(self):
        super().__init__()

        if self.COMPOSE_FILE is None:
            raise Exception("COMPOSE_FILE is not defined")

        self._docker = DockerClient(compose_files=[self.COMPOSE_FILE])

    def _start_docker(self):
        self._docker.compose.up(detach=True, wait=True)

    def _close_docker(self):
        self._docker.compose.down()

    def _restart_docker(self):
        self._close_docker()
        self._start_docker()

    def start(self, reset=True):
        if reset:
            self._restart_docker()
        else:
            self._start_docker()

    def close(self):
        self._close_docker()