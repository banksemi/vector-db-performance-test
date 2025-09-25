import os
from abc import ABC, abstractmethod

from dotenv import dotenv_values
from python_on_whales import DockerClient
from src.databases.interface import Database


class DockerBasedDatabase(Database, ABC):
    DOCKER_FOLDER = None

    def __init__(self):
        super().__init__()

        if self.DOCKER_FOLDER is None:
            raise Exception("DOCKER_FOLDER is not defined")

        env_path = os.path.join(self.DOCKER_FOLDER, "config.env")
        env_files = [env_path] if os.path.exists(env_path) else []
        if env_files:
            self._env = dotenv_values(env_files[0])
        else:
            self._env = {}

        project_name = 'vector-test-' + os.path.basename(self.DOCKER_FOLDER)

        self._docker = DockerClient(
            compose_files=[os.path.join(self.DOCKER_FOLDER, "docker-compose.yaml")],
            compose_env_files=env_files,
            compose_project_name=project_name
        )

    def get_env_value(self, key: str):
        return self._env[key] # Raise KeyError

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