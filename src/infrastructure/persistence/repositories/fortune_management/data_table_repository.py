from typing import Optional, List

from sqlalchemy import func, desc, asc

from src.api.models.dto.adjust.data_table_request_dto import DataTableRequestDto
from src.api.models.dto.adjust.data_table_response_dto import DataTableResponseDto
from src.domain.adjust_data.entities.data_table import DataTable as DomainDataTable
from src.domain.adjust_data.repositories.data_table_repository import DataTableRepository as DataTableDomainRepository
from src.infrastructure.entities.adjust_management.data_table import DataTable
from src.infrastructure.persistence.repositories.base_repository import BaseGenericRepository


class DataTableRepository(BaseGenericRepository[DomainDataTable], DataTableDomainRepository):

    def __init__(self) -> None:
        super().__init__(DataTable, DomainDataTable)

    def get_data(self, data_request_schema: DataTableRequestDto) -> Optional[List[DataTableResponseDto]]:

        # query of what we get
        query = self.session.query(DataTable.date,
                                   DataTable.channel,
                                   DataTable.country,
                                   DataTable.os,
                                   func.sum(DataTable.clicks).label("clicks"),
                                   func.sum(DataTable.impressions).label("impressions"),
                                   func.sum(DataTable.installs).label("installs"),
                                   func.sum(DataTable.spend).label("spend"),
                                   func.sum(DataTable.revenue).label("revenue"),
                                   func.avg(DataTable.spend / DataTable.installs).label("cpi"))

        # add time filter to query
        query_filter_with_time = query.filter(DataTable.date >= data_request_schema.date_from,
                                              DataTable.date < data_request_schema.date_to)

        # add other filters to query
        query_filter = query_filter_with_time
        for filter in data_request_schema.filter_metrics:
            if filter.get("filter_type") == "country":
                query_filter = query_filter.filter_by(country=filter.get("filter"))
            elif filter.get("filter_type") == "channel":
                query_filter = query_filter.filter_by(channel=filter.get("filter"))
            elif filter.get("filter_type") == "os":
                query_filter = query_filter.filter_by(os=filter.get("filter"))

        # group to query
        query_group = query_filter
        # if there is any column for grouping
        if len(data_request_schema.group_with) > 0:
            query_group = query_filter \
                .group_by(*data_request_schema.group_with)

        # all sorting with direction
        result = query_group
        for sort_col in data_request_schema.sort_column:
            if sort_col.get("direction") == "asc":
                result = query_group.order_by(asc(sort_col.get("sort_column")))
            elif sort_col.get("direction") == "desc":
                result = query_group.order_by(desc(sort_col.get("sort_column")))

        results = result.all()
        return [DataTableResponseDto.create_data(res) for res in results]
