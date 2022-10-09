import logging
from typing import Optional, List
from datetime import datetime

from src.api.models.dto.fortune.data_table_request_dto import DataTableRequestDto
from src.api.services.base.base_service import BaseService
from src.domain.adjust_data.entities.data_table import DataTable
from src.domain.seed_work.repository.unit_of_work import UnitOfWork

from src.api.services.base.base_adjust_api_service import BaseAdjustDataApiService


class AdjustDataApiService(BaseAdjustDataApiService, BaseService):
    logger = logging.getLogger(__name__)

    def __init__(self, uow: Optional[UnitOfWork] = None) -> None:
        super().__init__(uow)

    def get_random_data(self, data_request: DataTableRequestDto) -> Optional[List[DataTable]]:
        """
        Returns a random adjust_data
        """
        adjust_data = self.uow.data_table.get_data(data_request)
        if adjust_data:
            return adjust_data

        return None
