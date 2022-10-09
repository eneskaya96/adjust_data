from flask import Response
from flask_restx import Namespace, Resource

from src.api.controllers import create_schemas
from src.api.controllers.adjust_data import auth
from src.api.models.base_response import BaseResponse
from src.api.models.dto.fortune.data_table_request_dto import DataTableRequestDto
from src.api.models.dto.fortune.data_table_response_dto import DataTableResponseDto
from src.api.services.adjust_data_service import AdjustDataApiService

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
    BaseResponse[DataTableResponseDto].schema()
)


@api.route('')
class FortuneCRUD(Resource):
    @api.doc(description='Returns random adjust_data', security='api_key')
    @api.response(200, 'OK', data_response_schema)
    @auth.login_required
    def get(self) -> Response:
        adjust_data_api_service = AdjustDataApiService()
        data = adjust_data_api_service.get_random_data()
        data_response_dto = DataTableResponseDto.create(data)
        return BaseResponse.create_response(message='Data obtained.', data=data_response_dto)
