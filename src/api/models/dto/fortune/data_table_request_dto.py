from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel
from datetime import date


class DataTableRequestDto(BaseModel):
    date_to: Optional[date]
    date_from: Optional[date]
    filter_metrics: List[Dict[str, str]]
    group_with: List[str]
    sort_column: List[Dict[str, str]]  # Dict( sort column , direction)
    selected_columns: List[str]

