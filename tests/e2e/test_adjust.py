from datetime import date

import pytest
from flask.testing import FlaskClient

from src.api.models.dto.adjust.data_table_request_dto import DataTableRequestDto
from tests.e2e import get_api_url, get_authorization, get_base_response


@pytest.mark.usefixtures('db_session', 'client', 'uow')
class TestAdjust:

    @staticmethod
    def test_get_data(client: FlaskClient):

        data_request_dto = DataTableRequestDto(
            date_to=date(2017, 6, 1),
            date_from=date(2017, 5, 1),
            filter_metrics=[],
            group_with=["channel", "country"],
            sort_column=[{"sort_column": "clicks", "direction": "desc"}],
            selected_columns=["impressions", "clicks"]
        )

        response = client.post(get_api_url(f'/data'),
                               headers={'Authorization': get_authorization()},
                               json=data_request_dto.dict())
        base_response = get_base_response(response)

        assert base_response.success
