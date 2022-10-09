from pydantic import BaseSettings, Field
from typing import Optional
import logging


class BaseConfig(BaseSettings):
    """Base Configuration"""

    ENVIRONMENT: Optional[str] = Field('dev', env='ENVIRONMENT')

    """Secrets"""

    GRAYLOG_IP: Optional[str]
    GRAYLOG_PORT: Optional[int]

    AUTH_USERNAME: Optional[str]
    AUTH_PASSWORD: Optional[str]


    """Configurations"""
    ENABLE_GRAYLOG: Optional[bool] = Field(True)
    GRAYLOG_LOGGING_LEVEL: int = Field(logging.INFO)
