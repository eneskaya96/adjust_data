from typing import Optional, List

from sqlalchemy import func, desc

from src.api.models.dto.fortune.data_table_request_dto import DataTableRequestDto
from src.domain.adjust_data.entities.data_table import DataTable as DomainDataTable
from src.domain.adjust_data.repositories.data_table_repository import DataTableRepository as DataTableDomainRepository
from src.infrastructure.entities.adjust_management.data_table import DataTable
from src.infrastructure.persistence.repositories.base_repository import BaseGenericRepository


class DataTableRepository(BaseGenericRepository[DomainDataTable], DataTableDomainRepository):

    def __init__(self) -> None:
        super().__init__(DataTable, DomainDataTable)

    def get_data(self, data_request_schema: DataTableRequestDto) -> Optional[List[DataTable]]:
        # .group_by(data_request_schema.group_with[0]) \
        # self.query

        # query of what we get
        query = self.session.query(DataTable.channel,
                                   DataTable.country,
                                   func.sum(DataTable.impressions).label("impressions"),
                                   func.sum(DataTable.clicks).label("clicks"))

        # add time filter to query
        query_filter_with_time = query.filter(DataTable.date > data_request_schema.date_from,
                                              DataTable.date < data_request_schema.date_to)

        # add other filters to query
        query_filter = query_filter_with_time
        for filter in data_request_schema.filter_metrics:
            if filter.get("filter_type") == "country":
                query_filter = query_filter.filter_by(country=filter.get("filter"))

        # group to query
        query_group = query_filter \
            .group_by(*data_request_schema.group_with)

        results = query_group.order_by(desc(data_request_schema.sort_column)).all()

        return [DomainDataTable.parse_obj(data) for data in results]
