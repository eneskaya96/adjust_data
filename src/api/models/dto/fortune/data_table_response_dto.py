from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class DataTableResponseDto(BaseModel):
    date: Optional[str] = None
    channel: Optional[str] = None
    country: Optional[str] = None
    os: Optional[str] = None

    clicks: Optional[int] = None
    impressions: Optional[int] = None
    installs: Optional[int] = None
    spend: Optional[float] = None
    revenue: Optional[float] = None
    cpi: Optional[float] = None

