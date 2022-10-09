from flask import Blueprint
from flask_httpauth import HTTPBasicAuth

from src.configs.config_manager import ApiConfigManager

adjust_api = Blueprint('adjust_api', __name__, url_prefix='/adjust_api/v1')

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username: str, password: str) -> bool:
    return username == ApiConfigManager.config.AUTH_USERNAME and password == ApiConfigManager.config.AUTH_PASSWORD
