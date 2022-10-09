from dependency_injector import containers, providers

from src.domain.adjust_data.services.adjust_data_service import DataTableService

from src.infrastructure.persistence.repositories.unit_of_work import UnitOfWork


class BaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()


class Repositories(BaseContainer):
    unit_of_work = providers.Factory(UnitOfWork)


class Services(BaseContainer):
    fortune_service = providers.Factory(DataTableService)
