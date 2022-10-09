import logging
import graypy

from src.configs.api_config import GlobalConfig


class LogManager:
    is_graylog_initialized: bool = False

    @classmethod
    def init_logger(cls, config: GlobalConfig) -> None:
        cls.is_graylog_initialized = False
        logger = logging.getLogger()

        logger.setLevel(config.GRAYLOG_LOGGING_LEVEL)
        logging.getLogger('apscheduler').setLevel(logging.INFO)

        if config.GRAYLOG_IP and config.GRAYLOG_PORT:
            handler = graypy.GELFUDPHandler(config.GRAYLOG_IP, config.GRAYLOG_PORT)
            logger.addHandler(handler)

            logger.info('GrayLog has been initialised.')

            cls.is_graylog_initialized = True
