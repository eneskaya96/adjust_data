from logging import Filter, LogRecord
from typing import Optional


from src.configs.config_manager import BaseConfigManager, BaseConfig


class EnvironmentFilter(Filter):
    config: Optional[BaseConfig] = None

    def filter(self, record: LogRecord) -> bool:
        if not self.config:
            self.config = BaseConfigManager.config
        record.environment = self.config.ENVIRONMENT or 'dev'

        return True
