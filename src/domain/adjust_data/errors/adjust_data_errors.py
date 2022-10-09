import logging
from http import HTTPStatus
from typing import Optional, Dict, Any

from src.domain.seed_work.error.base_error import BaseError


class BaseAdjustDataError(BaseError):
    def __init__(self, message: str, error_code: str, status_code: int = HTTPStatus.BAD_REQUEST,
                 log_level: int = logging.CRITICAL,  context_data: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, error_code, status_code, log_level, context_data)


class InvalidDateError(BaseAdjustDataError):
    code = 'invalid_date'

    def __init__(self, **context_data: Any) -> None:
        super().__init__('Invalid date.', self.code, context_data=context_data)

