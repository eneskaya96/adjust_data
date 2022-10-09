from typing import Any

from flask import Flask, request
from flask_httpauth import HTTPBasicAuth

from src.configs.api_config import GlobalConfig


class BasicAuthManager:

    @classmethod
    def init_basic_auth_manager(cls, app: Flask, config: GlobalConfig) -> None:
        auth = HTTPBasicAuth()

        @auth.verify_password
        def verify_password(username: str, password: str) -> bool:
            return username == config.SWAGGER_USERNAME and password == config.SWAGGER_PASSWORD

        @app.before_request
        def check_security_for_swagger() -> Any:
            if (
                    request.path in ('/api/v1/', '/captcha/v1/', '/maintainer/v1/', '/test/v1/') or
                    'swagger' in request.path
            ):
                # Do not enforce basic auth for local env
                if config.ENVIRONMENT == 'local' or auth.authenticate(request.authorization, None):
                    return

                # If the requester IP address in enabled_ips do not enforce basic auth
                view = app.view_functions[request.endpoint]
                return auth.login_required(view)()
