from typing import Callable, Optional
from dependency_injector.wiring import Provider

from src.api.injection.containers import Repositories
from src.api.services.base.base_api_services import BaseApiServices
from src.domain.seed_work.repository.unit_of_work import UnitOfWork


class BaseService:
    uow_provider: Callable[..., UnitOfWork] = Provider[Repositories.unit_of_work]

    def __init__(self, uow: Optional[UnitOfWork] = None) -> None:
        self._uow: Optional[UnitOfWork] = uow
        self._services: Optional[BaseApiServices] = None

    @property
    def uow(self) -> UnitOfWork:
        if not self._uow:
            self._uow = self.uow_provider()
        return self._uow

    @property
    def services(self) -> BaseApiServices:
        if not self._services:
            # Imported here to prevent cyclic import
            from src.api.services.api_services import ApiServices
            self._services = ApiServices(self._uow)
        return self._services
