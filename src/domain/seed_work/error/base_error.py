import logging
from http import HTTPStatus
from typing import Optional, Dict, Any


class BaseError(Exception):
    def __init__(self, message: str, error_code: str,
                 status_code: int = HTTPStatus.OK, log_level: int = logging.ERROR,
                 context_data: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.log_level = log_level
        self.context_data = context_data
        super().__init__(message)
