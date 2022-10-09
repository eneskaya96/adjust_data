from typing import Optional

from flask import Flask
from flask_restx import Api

from src.api.controllers.adjust_data import adjust_api
from src.api.controllers.adjust_data.data_controller import api as data_api


class APIManager:
    def __init__(self, app: Flask) -> None:
        self.api: Optional[Api] = None
        self.init_apis(app)

    def init_apis(self, app: Flask) -> None:
        self.api = Api(
            adjust_api,
            title='SaaS Adjust API',
            version='0.0.1',
            description='Provides functionalities for Saas'
        )

        self.api.add_namespace(data_api)

        app.register_blueprint(adjust_api)
