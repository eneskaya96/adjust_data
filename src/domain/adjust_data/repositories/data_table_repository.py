import abc
from typing import Optional, List

from src.api.models.dto.adjust.data_table_request_dto import DataTableRequestDto
from src.api.models.dto.adjust.data_table_response_dto import DataTableResponseDto
from src.domain.seed_work.repository.base_repository import BaseRepository
from src.domain.adjust_data.entities.data_table import DataTable


class DataTableRepository(BaseRepository[DataTable], abc.ABC):
    @abc.abstractmethod
    def get_data(self, data_request_schema: DataTableRequestDto) -> Optional[List[DataTableResponseDto]]:
        pass
