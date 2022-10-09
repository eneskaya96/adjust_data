from http import HTTPStatus

from src.domain.seed_work.error.base_error import BaseError


class ConfigurationError(BaseError):
    def __init__(self, message: str, error_code: str, status_code: int = HTTPStatus.OK) -> None:
        super().__init__(message, error_code, status_code, log_level=True)
