import logging
from typing import Optional, List

from src.api.models.dto.adjust.data_table_request_dto import DataTableRequestDto
from src.api.models.dto.adjust.data_table_response_dto import DataTableResponseDto
from src.api.services.base.base_service import BaseService
from src.domain.adjust_data.errors.adjust_data_errors import InvalidDateError
from src.domain.seed_work.repository.unit_of_work import UnitOfWork

from src.api.services.base.base_adjust_api_service import BaseAdjustDataApiService


class AdjustDataApiService(BaseAdjustDataApiService, BaseService):
    logger = logging.getLogger(__name__)

    def __init__(self, uow: Optional[UnitOfWork] = None) -> None:
        super().__init__(uow)

    def get_data(self, data_request: DataTableRequestDto) -> Optional[List[DataTableResponseDto]]:
        """
        Returns a random adjust_data
        """
        # date range should be given
        if not data_request.date_to or not data_request.date_from:
            raise InvalidDateError()

        # we can modified the response for just returning group elements and selected columns
        # front end should just show the grouping columns and wanted results
        adjust_data_all = self.uow.data_table.get_data(data_request)
        if adjust_data_all:
            return adjust_data_all

        return None
