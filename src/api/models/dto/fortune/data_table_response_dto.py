from __future__ import annotations
from pydantic import BaseModel
from src.domain.adjust_data.entities.data_table import DataTable


class DataTableResponseDto(BaseModel):
    clicks: int
    date: str
    channel: str
    country: str
    os: str
    impressions: int
    installs: int
    spend: float
    revenue: float

    @classmethod
    def create(cls, data: DataTable) -> DataTableResponseDto:
        return cls(
            clicks=data.clicks,
            date=str(data.date),
            channel=data.channel,
            country=data.country,
            os=data.os,
            impressions=data.impressions,
            installs=data.installs,
            spend=data.spend,
            revenue=data.revenue
        )
