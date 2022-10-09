from typing import List

from src.api import services, controllers
from src.api.injection.containers import BaseContainer, Repositories, Services
from src.configs.config_manager import ApiConfigManager


class ContainerManager:
    _containers: List[BaseContainer] = []
    repositories: Repositories
    services: Services

    @classmethod
    def init_containers(cls) -> List[BaseContainer]:
        cls.repositories = Repositories()
        cls.services = Services()

        cls._init_container(cls.repositories)
        cls._init_container(cls.services)

        cls._containers = [cls.repositories, cls.services]
        return cls._containers

    @classmethod
    def unwire_containers(cls) -> None:
        for container in cls._containers:
            container.unwire()

    @classmethod
    def _init_container(cls, container: BaseContainer) -> None:
        container.init_resources()
        container.config.from_pydantic(ApiConfigManager.config)
        container.wire(packages=[services, controllers])
