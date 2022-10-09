from dataclasses import dataclass
from datetime import date
from src.infrastructure.entities.base_entity import BaseStrEntity


@dataclass
class DataTable(BaseStrEntity):
    clicks: int
    date: date
    channel: str
    country: str
    os: str
    impressions: int
    installs: int
    spend: float
    revenue: float
