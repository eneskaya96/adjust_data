from __future__ import annotations

from typing import Dict, List, Optional, Any

from pydantic import BaseModel
from datetime import date


class DataTableRequestDto(BaseModel):
    date_to: Optional[date]
    date_from: Optional[date]
    filter_metrics: List[Dict[str, str]]
    group_with: List[str]
    sort_column: List[Dict[str, str]]  # Dict( sort column , direction)
    selected_columns: List[str]

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return {
            'date_to': self.date_to.strftime("%Y-%m-%d") or None,
            'date_from': self.date_from.strftime("%Y-%m-%d") or None,
            'filter_metrics': self.filter_metrics or [],
            'group_with': self.group_with or [],
            'sort_column': self.sort_column or [],
            'selected_columns': self.selected_columns or []
        }