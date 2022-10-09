import os
from pathlib import Path
from typing import Optional

from pydantic import Field, Extra

# get root directory: root/src/api_config.py -> root
# then create envs directory: root/envs/
from src.configs.base_config import BaseConfig

envs_dir = os.path.join(Path(__file__).parent.parent.parent.absolute(), 'envs')


class GlobalConfig(BaseConfig):
    """Global Configuration"""

    """Secrets"""

    MYSQL_HOST: Optional[str]
    MYSQL_PASSWORD: Optional[str]
    MYSQL_USER: Optional[str]
    MYSQL_DB_NAME: Optional[str]

    SWAGGER_USERNAME: Optional[str]
    SWAGGER_PASSWORD: Optional[str]

    SALT_SECRET_KEY: str = Field('\x1bEy6\xcc\x96\x16\xb3E!\xec\xd6\xb3M\xcf\x90')

    """Configurations"""
    PROPAGATE_EXCEPTIONS: Optional[bool] = Field(True)  # must be true to return api errors
    DOMAIN_NAME: Optional[str]

    SQLALCHEMY_DATABASE_URI: Optional[str]

    DB_POOL_RECYCLE: int = Field(60 * 60)  # recycle intervals in seconds
    DB_POOL_SIZE: int = Field(40)
    DB_MAX_OVERFLOW: int = Field(50)
    DB_POOL_TIMEOUT: int = Field(1)  # timeout in seconds for obtain a connection from pool
    DB_LOGGING: bool = Field(False)

    class Config:
        extra = Extra.allow

    def create_db_uri(self) -> str:
        self.SQLALCHEMY_DATABASE_URI \
            = f'mysql+mysqldb://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}/{self.MYSQL_DB_NAME}?charset=utf8mb4'
        return self.SQLALCHEMY_DATABASE_URI


class LocalConfig(GlobalConfig):
    """Local Configuration"""

    class Config:
        env_file: str = os.path.join(envs_dir, 'local.env')


class DevConfig(GlobalConfig):
    """Development Configuration"""

    class Config:
        env_file: str = os.path.join(envs_dir, 'dev.env')


class StagingConfig(GlobalConfig):
    """Staging Configuration"""

    class Config:
        env_file: str = os.path.join(envs_dir, 'staging.env')


class ProdConfig(GlobalConfig):
    """Production Configuration"""

    class Config:
        env_file: str = os.path.join(envs_dir, 'prod.env')


class TestConfig(GlobalConfig):
    """Test Configuration"""

    class Config:
        env_file: str = os.path.join(envs_dir, 'test.env')


class FactoryConfig:
    """Returns a config instance depending on the ENVIRONMENT variable."""

    def __init__(self, environment: Optional[str]) -> None:
        self.environment = environment

    def __call__(self) -> GlobalConfig:
        if self.environment == "local":
            return LocalConfig()

        elif self.environment == "dev":
            return DevConfig()

        elif self.environment == "staging":
            return StagingConfig()

        elif self.environment == "prod":
            return ProdConfig()

        elif self.environment == "test":
            return TestConfig()

        else:
            return GlobalConfig()
