import abc

from src.api.services.base.base_adjust_api_service import BaseAdjustDataApiService


class BaseApiServices(abc.ABC):
    @property
    @abc.abstractmethod
    def data_table(self) -> BaseAdjustDataApiService:
        pass
