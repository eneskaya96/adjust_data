import abc
from typing import Optional, List, TypeVar, Generic, Union

from src.domain.seed_work.model.base_entity_model import BaseEntityModel

EType = TypeVar('EType', bound=BaseEntityModel)


class BaseRepository(Generic[EType], abc.ABC):

    @abc.abstractmethod
    def insert(self, entity: EType) -> None:
        pass

    @abc.abstractmethod
    def insert_many(self, entities: List[EType]) -> None:
        pass

    @abc.abstractmethod
    def update(self, entity: EType) -> None:
        pass

    @abc.abstractmethod
    def upsert(self, entity: EType) -> None:
        pass

    @abc.abstractmethod
    def delete(self, entity: EType) -> None:
        pass

    @abc.abstractmethod
    def delete_by_id(self, entity_id: Union[str, int]) -> None:
        pass

    @abc.abstractmethod
    def delete_list(self, entity_ids: Union[List[str], List[int]]) -> None:
        pass

    @abc.abstractmethod
    def get(self, entity_id: Union[str, int]) -> Optional[EType]:
        pass

    @abc.abstractmethod
    def get_list(self, entity_ids: Union[List[str], List[int]]) -> List[EType]:
        pass

    @abc.abstractmethod
    def all(self) -> List[EType]:
        pass

    @abc.abstractmethod
    def last(self) -> Optional[EType]:
        pass
