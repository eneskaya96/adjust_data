from typing import List, Any

from flask_restx import Namespace

from src.api.models.dto.adjust.data_table_request_dto import DataTableRequestDto
from src.api.models.dto.adjust.data_table_response_dto import DataTableResponseDto


# define model schemas here to register them only once. auth_controller registers these schemas.
def create_schemas(api: Namespace) -> List[Any]:
    return [
        # request dtos
        api.schema_model('DataTableRequestDto', DataTableRequestDto.schema()),

        # response dtos
        api.schema_model('DataTableResponseDto', DataTableResponseDto.schema()),

        # domain models
    ]
