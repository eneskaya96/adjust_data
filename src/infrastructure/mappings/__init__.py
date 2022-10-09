import abc
from typing import Dict

from sqlalchemy import Table, MetaData


class BaseMapper(abc.ABC):
    def __init__(self, metadata: MetaData, entity_type: type):
        self._metadata = metadata
        self._entity_type = entity_type

    def map(self, mappings: Dict[type, Table]) -> Table:
        mapping = self.perform_mapping(mappings)

        mappings[self._entity_type] = mapping

        return mapping

    @abc.abstractmethod
    def perform_mapping(self, mappings: Dict[type, Table]) -> Table:
        pass
