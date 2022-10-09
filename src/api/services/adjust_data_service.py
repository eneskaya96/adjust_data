import logging
from typing import Optional, List

from src.api.models.dto.fortune.data_table_request_dto import DataTableRequestDto
from src.api.models.dto.fortune.data_table_response_dto import DataTableResponseDto
from src.api.services.base.base_service import BaseService
from src.domain.adjust_data.entities.data_table import DataTable
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

        response_dto_list = []
        adjust_data_all = self.uow.data_table.get_data(data_request)
        if adjust_data_all:
            for adjust_data in adjust_data_all:
                response_dto = DataTableResponseDto()
                for gr in data_request.group_with:
                    if gr == "date":
                        response_dto.date = adjust_data[0]
                    elif gr == "channel":
                        response_dto.channel = adjust_data[1]
                    elif gr == "country":
                        response_dto.country = adjust_data[2]
                    elif gr == "os":
                        response_dto.os = adjust_data[3]

                for sc in data_request.selected_columns:
                    if sc == "clicks":
                        response_dto.clicks = adjust_data[4]
                    elif sc == "impressions":
                        response_dto.impressions = adjust_data[5]
                    elif sc == "installs":
                        response_dto.installs = adjust_data[6]
                    elif sc == "spend":
                        response_dto.spend = adjust_data[7]
                    elif sc == "revenue":
                        response_dto.revenue = adjust_data[8]
                    elif sc == "cpi":
                        response_dto.cpi = adjust_data[7] / adjust_data[6]

                response_dto_list.append(response_dto)
            return response_dto_list

        return None
