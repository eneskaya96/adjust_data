import abc

from src.configs.base_config import BaseConfig
from src.configs.api_config import FactoryConfig as ApiFactoryConfig, GlobalConfig as ApiGlobalConfig


class BaseConfigManager(abc.ABC):
    config: BaseConfig

    @classmethod
    @abc.abstractmethod
    def init_config(cls) -> BaseConfig:
        pass


class ApiConfigManager(BaseConfigManager):
    config: ApiGlobalConfig

    @classmethod
    def init_config(cls) -> ApiGlobalConfig:
        cls.config = ApiFactoryConfig(BaseConfig().ENVIRONMENT)()
        BaseConfigManager.config = cls.config
        cls.config.create_db_uri()
        return cls.config
