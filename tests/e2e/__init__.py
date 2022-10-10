import base64

from flask import json, Response

from src.api.models.base_response import BaseResponse
from src.configs.config_manager import BaseConfigManager


def get_authorization() -> str:
    encoded_auth_bytes = base64.b64encode(
        f'{BaseConfigManager.config.AUTH_USERNAME}:{BaseConfigManager.config.AUTH_PASSWORD}'.encode('utf-8'))
    encoded_auth_str = str(encoded_auth_bytes, 'utf-8')
    return f'Basic {encoded_auth_str}'


def get_api_url(url: str) -> str:
    return f'/adjust_api/v1{url}'


def get_base_response(response: Response) -> BaseResponse:
    response_json = json.loads(response.data)
    return BaseResponse(**response_json)
