from typing import Dict

from sqlalchemy import MetaData
from sqlalchemy.schema import Table

from src.infrastructure.mappings.adjust_management.data_table_mapper import DataTableMapper


class MapManager:
    _metadata: MetaData = None
    _mappings: Dict[type, Table] = {}

    @classmethod
    def map_entities(cls) -> MetaData:
        cls._metadata = MetaData()

        DataTableMapper(cls._metadata).map(cls._mappings)

        return cls._metadata
