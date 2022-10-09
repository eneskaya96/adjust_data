from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel


class DataTableRequestDto(BaseModel):
    adjust_data: str

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return {
            'adjust_data': self.adjust_data
        }
