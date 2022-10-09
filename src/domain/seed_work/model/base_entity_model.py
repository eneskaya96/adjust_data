from datetime import datetime
from typing import Optional, Any, Dict
from uuid import uuid4

from pydantic import BaseModel, Field, validator

from src.domain.seed_work.validator import check_guid, check_id


class BaseEntityModel(BaseModel):
    created_date: datetime = Field(default_factory=datetime.utcnow)
    modified_date: Optional[datetime] = None

    class Config:
        orm_mode = True

    def to_orm(self) -> Dict[str, Any]:
        return self.dict()


class BaseStrEntityModel(BaseEntityModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    # validators
    _check_guid_valid: classmethod = validator('id', allow_reuse=True)(check_guid)

    class Config:
        orm_mode = True


class BaseIntEntityModel(BaseEntityModel):
    id: int = 0

    # validators
    _check_id_valid: classmethod = validator('id', allow_reuse=True)(check_id)

    class Config:
        orm_mode = True
