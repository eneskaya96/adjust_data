from typing import List

from flask import Response
from flask_restx import Namespace, Resource

from src.api.controllers import create_schemas
from src.api.controllers.adjust_data import auth
from src.api.models.base_response import BaseResponse
from src.api.models.dto.adjust.data_table_request_dto import DataTableRequestDto
from src.api.models.dto.adjust.data_table_response_dto import DataTableResponseDto
from src.api.services.adjust_data_service import AdjustDataApiService
from flask import Response, request

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
    @api.expect(*used_schemas, data_request_schema)
    @api.response(200, 'OK', data_response_schema)
    @auth.login_required
    def post(self) -> Response:
        data = request.get_json()
        data_request_dto = DataTableRequestDto.parse_obj(data)

        adjust_data_api_service = AdjustDataApiService()
        data = adjust_data_api_service.get_data(data_request_dto)
        return BaseResponse.create_response(message='Data obtained.', data=data)
