import abc

from src.api.models.dto.fortune.data_table_request_dto import DataTableRequestDto
from src.domain.adjust_data.entities.data_table import DataTable


class BaseAdjustDataApiService(abc.ABC):
    @abc.abstractmethod
    def get_data(self, data_request: DataTableRequestDto) -> DataTable:
        pass
