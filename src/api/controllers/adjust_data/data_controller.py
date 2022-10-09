from typing import List

from flask import Response
from flask_restx import Namespace, Resource

from src.api.controllers import create_schemas
from src.api.controllers.adjust_data import auth
from src.api.models.base_response import BaseResponse
from src.api.models.dto.fortune.data_table_request_dto import DataTableRequestDto
from src.api.models.dto.fortune.data_table_response_dto import DataTableResponseDto
from src.api.services.adjust_data_service import AdjustDataApiService
from datetime import datetime

api = Namespace('data', description='API for data')

used_schemas = create_schemas(api)

# request dto
data_request_schema = api.schema_model(
    'data_request_schema',
    DataTableRequestDto.schema()
)
# response dto
data_response_schema = api.schema_model(
    'data_response_schema',
    BaseResponse[List[DataTableResponseDto]].schema()
)


@api.route('')
class FortuneCRUD(Resource):
    @api.doc(description='Returns random adjust_data', security='api_key')
    @api.response(200, 'OK', data_response_schema)
    @auth.login_required
    def post(self) -> Response:
        data_request_schema = DataTableRequestDto(
            date_to=datetime(2017, 6, 1),
            date_from=datetime(2017, 5, 1),
            filter_metrics=[],
            group_with=["channel", "country"],
            sort_column=[{"sort_column": "clicks", "direction": "desc"}],
            selected_columns=["impressions", "clicks"]
        )

        adjust_data_api_service = AdjustDataApiService()
        data = adjust_data_api_service.get_data(data_request_schema)
        return BaseResponse.create_response(message='Data obtained.', data=data)
