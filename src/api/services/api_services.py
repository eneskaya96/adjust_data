from typing import Optional

from src.api.services.base.base_api_services import BaseApiServices
from src.api.services.adjust_data_service import AdjustDataApiService
from src.domain.seed_work.repository.unit_of_work import UnitOfWork


class ApiServices(BaseApiServices):
    def __init__(self, uow: Optional[UnitOfWork] = None) -> None:
        self._uow: Optional[UnitOfWork] = uow
        self.adjust_api_service: Optional[AdjustDataApiService] = None

    @property
    def fortune(self) -> AdjustDataApiService:
        if not self.adjust_api_service:
            self.adjust_api_service = AdjustDataApiService(self._uow)
        return self.adjust_api_service
