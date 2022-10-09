import logging
from typing import Any, Optional, Type, Dict
from uuid import uuid4

from sqlalchemy.orm import Session

from src.domain.seed_work.repository.unit_of_work import UnitOfWork as BaseDomainUnitOfWork
from src.infrastructure.db.db_manager import DBManager
from src.domain.adjust_data.repositories import data_table_repository
from src.infrastructure.persistence.repositories.fortune_management.data_table_repository import DataTableRepository
from src.infrastructure.persistence.repositories.base_repository import TRepo


class UnitOfWork(BaseDomainUnitOfWork):
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self._session_uuid: Optional[str] = None
        self._session: Optional[Session] = None
        self._depth = 0
        self._repositories: Dict[str, Any] = {}

        super().__init__()

    def __enter__(self) -> BaseDomainUnitOfWork:
        self.logger.debug(f'Entering UOW context with id {self._session_uuid} '
                          f'from depth {self._depth} to {self._depth + 1}')
        self._depth += 1
        self._session = self.session  # Creates a new UOW session if non exists and depth is more than 0
        return super().__enter__()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.logger.debug(f'Exiting UOW context with id {self._session_uuid} '
                          f'from depth {self._depth} to {self._depth - 1}')
        self._depth -= 1
        if self._depth == 0:
            self.logger.debug(f'UOW context with id {self._session_uuid} is reached to depth 0,'
                              f' exiting the UOW context completely.')
            super().__exit__(exc_type, exc_val, exc_tb)
            self.close()

    # region Subscription Repositories
    @property
    def data_table(self) -> data_table_repository.DataTableRepository:
        return self.__get_repository(DataTableRepository)(self.session, not self._depth)

    # endregion

    @property
    def session(self) -> Session:
        if not self._session:
            if self._depth > 0:
                self._session = DBManager.new_session()
                self._session_uuid = str(uuid4())
                self.logger.debug(f'Created a new session for UOW context with id {self._session_uuid}')
            else:
                self.logger.debug(f'Created a scoped session for outside of UOW context')
                return DBManager.new_scoped_session()
        return self._session

    def commit(self) -> None:
        self.logger.debug(f'Committed the session for UOW context with id {self._session_uuid}')
        self.session.commit()

    def rollback(self) -> None:
        self.logger.debug(f'Rolled back the session for UOW context with id {self._session_uuid}')
        self.session.rollback()

    def is_in_context(self) -> bool:
        return self._depth > 0

    def close(self) -> None:
        if self._session:  # pragma: no cover
            self.logger.debug(f'Closing the session of UOW context with id {self._session_uuid}')
            self._session.close()
            self._session = None

    def __get_repository(self, repo_type: Type[TRepo]) -> TRepo:
        repository = self._repositories.get(repo_type.__name__)
        if not repository:
            repository = repo_type()  # type: ignore
            self._repositories[repo_type.__name__] = repository
        return repository
