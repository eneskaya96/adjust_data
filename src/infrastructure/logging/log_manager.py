import logging

import graypy

from src.configs.base_config import BaseConfig
from src.infrastructure.logging.environment_filter import EnvironmentFilter


class LogManager:
    is_graylog_initialized: bool = False

    @classmethod
    def init_logger(cls, config: BaseConfig) -> None:
        cls.is_graylog_initialized = False
        logger = logging.getLogger()

        logger.setLevel(config.GRAYLOG_LOGGING_LEVEL)
        logging.getLogger('werkzeug').setLevel(config.GRAYLOG_LOGGING_LEVEL)

        if (config.ENABLE_GRAYLOG and config.ENVIRONMENT in ['local', 'dev', 'staging', 'prod']
                and config.GRAYLOG_IP and config.GRAYLOG_PORT):
            handler = graypy.GELFUDPHandler(config.GRAYLOG_IP, config.GRAYLOG_PORT)

            environment_filter = EnvironmentFilter()
            handler.addFilter(environment_filter)

            logger.addHandler(handler)

            logger.info('GrayLog has been initialised.')

            cls.is_graylog_initialized = True
