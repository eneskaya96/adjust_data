from __future__ import annotations

import logging
from datetime import datetime
from typing import List, TypeVar, Type, Generic, Optional, Union

from sqlalchemy import func, desc
from sqlalchemy.orm import Session, Query
from sqlalchemy.sql import operators

from src.domain.seed_work.repository.base_repository import BaseRepository as BaseDomainRepository, EType
from src.infrastructure.entities.base_entity import BaseEntity
from src.infrastructure.db.db_manager import DBManager

TRepo = TypeVar('TRepo', bound='BaseRepository')


class BaseRepository:
    def __init__(self, entity_type: Type[BaseEntity]):
        self._session: Optional[Session] = None
        self._auto_commit = False
        self.entity_type = entity_type

    def __call__(self: TRepo, session: Session, auto_commit: bool = False) -> TRepo:
        self._session = session
        self._auto_commit = auto_commit
        return self

    @property
    def session(self) -> Session:
        if not self._session:
            self._session = DBManager.new_scoped_session()
        return self._session

    @property
    def query(self) -> Query:
        return self.session.query(self.entity_type)

    def commit(self) -> None:
        if self._auto_commit:
            self.session.commit()

    @staticmethod
    def get_count(count_query: Query) -> int:
        query = count_query.statement.with_only_columns([func.count()])
        return count_query.session.execute(query).scalar()

    @staticmethod
    def exists(exists_query: Query) -> bool:
        return exists_query.session.query(exists_query.exists()).scalar()


class BaseGenericRepository(BaseRepository, BaseDomainRepository[EType], Generic[EType]):
    def __init__(self, entity_type: Type[BaseEntity], domain_type: Type[EType]) -> None:
        self.logger = logging.getLogger(__name__)
        self._session: Optional[Session] = None
        self.entity_type = entity_type
        self.domain_type = domain_type
        super().__init__(entity_type)

    def insert(self, entity: EType) -> None:
        db_entity = self.entity_type.from_dict(entity.to_orm())
        self.session.add(db_entity)
        self.commit()

    def insert_many(self, entities: List[EType]) -> None:
        db_entities = [self.entity_type.from_dict(entity.to_orm()) for entity in entities]
        self.session.add_all(db_entities)
        self.commit()

    def update(self, entity: EType) -> None:
        db_entity = self.entity_type.from_dict(entity.to_orm())
        db_entity.modified_date = datetime.utcnow()
        self.session.merge(db_entity)
        self.commit()

    def upsert(self, entity: EType) -> None:
        db_entity = self.entity_type.from_dict(entity.to_orm())
        entity_from_db = self.get(db_entity.id)
        if entity_from_db:
            self.session.merge(db_entity)
        else:
            self.session.add(db_entity)
        self.commit()

    def delete(self, entity: EType) -> None:
        db_entity = self.entity_type.from_dict(entity.to_orm())
        self.session.delete(db_entity)
        self.commit()

    def delete_by_id(self, entity_id: Union[str, int]) -> None:
        self.query.filter(self.entity_type.id == entity_id).delete(synchronize_session=False)
        self.commit()

    def delete_list(self, entity_ids: Union[List[str], List[int]]) -> None:
        if not entity_ids:
            return

        self.query.filter(operators.in_op(self.entity_type.id, entity_ids)).delete(synchronize_session=False)
        self.commit()

    def get(self, entity_id: Union[str, int]) -> Optional[EType]:
        entity = self.query.get(entity_id)
        if not entity:
            return None
        return self.domain_type.from_orm(entity)

    def get_list(self, entity_ids: Union[List[str], List[int]]) -> List[EType]:
        if not entity_ids:
            return []

        entities = self.query.filter(operators.in_op(self.entity_type.id, entity_ids)).all()
        return [self.domain_type.from_orm(entity) for entity in entities]

    def all(self) -> List[EType]:
        entities = self.query.all()
        return [self.domain_type.from_orm(entity) for entity in entities]

    def last(self) -> Optional[EType]:
        entity = self.query.order_by(desc(self.entity_type.created_date)).limit(1).one_or_none()
        if not entity:
            return None
        return self.domain_type.from_orm(entity)
