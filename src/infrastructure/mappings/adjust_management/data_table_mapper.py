from typing import Dict

from sqlalchemy import MetaData, Table, Column, Integer, Float, String
from sqlalchemy.orm import mapper

from src.infrastructure.entities.adjust_management.data_table import DataTable
from src.infrastructure.mappings import BaseMapper


class DataTableMapper(BaseMapper):
    def __init__(self, metadata: MetaData):
        super().__init__(metadata, DataTable)

    def perform_mapping(self, mappings: Dict[type, Table]) -> Table:
        data_table_mapping = Table(
            'data_table', self._metadata,
            Column('id', Integer, primary_key=True),
            Column('clicks', Integer),
            Column('date', String(250)),
            Column('channel', String(250)),
            Column('country', String(250)),
            Column('os', String(250)),
            Column('impressions', Integer),
            Column('installs', Integer),
            Column('spend', Float),
            Column('revenue', Float)
        )

        mapper(DataTable, data_table_mapping)

        return data_table_mapping
