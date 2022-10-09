from typing import Optional

from src.domain.adjust_data.entities.data_table import DataTable as DomainDataTable
from src.domain.adjust_data.repositories.data_table_repository import DataTableRepository as DataTableDomainRepository
from src.infrastructure.entities.adjust_management.data_table import DataTable
from src.infrastructure.persistence.repositories.base_repository import BaseGenericRepository


class DataTableRepository(BaseGenericRepository[DomainDataTable], DataTableDomainRepository):

    def __init__(self) -> None:
        super().__init__(DataTable, DomainDataTable)

    def get_data(self) -> Optional[DataTable]:
        return self.query.first()
