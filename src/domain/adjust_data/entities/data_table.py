from __future__ import annotations

from src.domain.seed_work.model.base_entity_model import BaseStrEntityModel


class DataTable(BaseStrEntityModel):
    clicks: int
    date: date
    channel: str
    country: str
    os: str
    impressions: int
    installs: int
    spend: float
    revenue: float

    class Config:
        orm_mode = True

    @classmethod
    def create_data(cls,
                    clicks: int,
                    date: date,
                    channel: str,
                    country: str,
                    os: str,
                    impressions: int,
                    installs: int,
                    spend: float,
                    revenue: float) -> DataTable:
        return cls(clicks=clicks,
                   date=date,
                   channel=channel,
                   country=country,
                   os=os,
                   impressions=impressions,
                   installs=installs,
                   spend=spend,
                   revenue=revenue)
