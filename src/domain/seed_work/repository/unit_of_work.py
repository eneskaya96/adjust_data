from __future__ import annotations

import abc
import logging
from typing import Any

from src.domain.seed_work.error.integrity_error import IntegrityError
from src.domain.adjust_data.repositories import data_table_repository


class UnitOfWork(abc.ABC):
    logger = logging.getLogger(__name__)

    def __enter__(self) -> UnitOfWork:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        try:
            if not isinstance(exc_val, Exception):
                self.commit()
            else:
                self.rollback()
        except Exception as ex:
            self.logger.error('An error occurred performing a DB operation', exc_info=True)
            self.rollback()
            raise IntegrityError(
                message='An error occurred performing a DB operation'
            ) from ex

    @abc.abstractmethod
    def commit(self) -> None:
        pass

    @abc.abstractmethod
    def rollback(self) -> None:
        pass

    @abc.abstractmethod
    def is_in_context(self) -> bool:
        pass

    # region adjust_data Repositories
    @property
    @abc.abstractmethod
    def data_table(self) -> data_table_repository.DataTableRepository:
        pass

    # endregion
