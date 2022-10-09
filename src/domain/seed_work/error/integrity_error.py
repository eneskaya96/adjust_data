import logging
from http import HTTPStatus

from src.domain.seed_work.error.base_error import BaseError


class IntegrityError(BaseError):
    error_code = 'integrity_error'

    def __init__(self, message: str) -> None:
        super().__init__(message, self.error_code,
                         status_code=HTTPStatus.INTERNAL_SERVER_ERROR, log_level=logging.CRITICAL)
