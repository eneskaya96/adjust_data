import abc
from typing import Optional

from src.domain.seed_work.repository.base_repository import BaseRepository
from src.domain.adjust_data.entities.data_table import DataTable


class DataTableRepository(BaseRepository[DataTable], abc.ABC):
    @abc.abstractmethod
    def get_data(self) -> Optional[DataTable]:
        pass
