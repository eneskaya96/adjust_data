import abc

from src.domain.adjust_data.entities.data_table import DataTable


class BaseAdjustDataApiService(abc.ABC):
    @abc.abstractmethod
    def get_random_data(self) -> DataTable:
        pass
