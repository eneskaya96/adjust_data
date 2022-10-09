import logging
from typing import Optional
from datetime import datetime

from src.api.services.base.base_service import BaseService
from src.domain.adjust_data.entities.data_table import DataTable
from src.domain.seed_work.repository.unit_of_work import UnitOfWork

from src.api.services.base.base_adjust_api_service import BaseAdjustDataApiService


class AdjustDataApiService(BaseAdjustDataApiService, BaseService):
    logger = logging.getLogger(__name__)

    def __init__(self, uow: Optional[UnitOfWork] = None) -> None:
        super().__init__(uow)

    def get_random_data(self) -> DataTable:
        """
        Returns a random adjust_data
        """
        adjust_data = self.uow.data_table.get_data()
        if adjust_data:
            return adjust_data

        data = DataTable.create_data(1,
                                     datetime.utcnow().date(),
                                     "facebook",
                                     "TR",
                                     "ios",
                                     1,
                                     1,
                                     1.1,
                                     1.1)

        return data
