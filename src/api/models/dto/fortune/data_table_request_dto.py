from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel
from datetime import date


class DataTableRequestDto(BaseModel):
    date_to: Optional[date]
    date_from: Optional[date]
    filter_metrics: List[Dict[str, str]]
    group_with: List[str]
    sort_column: str
    desc: bool = True

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return {
            'date_to': self.date_to,
            'date_from': self.date_from,
            'filter_metrics': self.filter_metrics,
            'group_with': self.group_with,
            'sort_column': self.sort_column
        }
