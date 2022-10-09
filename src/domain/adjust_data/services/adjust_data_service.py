import logging
from src.domain.adjust_data.entities.data_table import DataTable

from datetime import datetime


class DataTableService:
    logger = logging.getLogger(__name__)

    @staticmethod
    def create_data() -> DataTable:
        return DataTable.create_data(1,
                                     datetime.utcnow().date(),
                                     "facebook",
                                     "TR",
                                     "ios",
                                     1,
                                     1,
                                     1.1,
                                     1.1)
