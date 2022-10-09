from __future__ import annotations

import logging
from http import HTTPStatus
from typing import Optional, TypeVar, Generic, Any

from flask import Response
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')
logger = logging.getLogger()


class BaseResponse(GenericModel, Generic[DataT]):
    success: bool = True
    message: Optional[str] = None
    code: Optional[str] = None
    data: Optional[DataT] = None

    @classmethod
    def create_response(cls,
                        success: bool = True,
                        message: Optional[str] = None,
                        code: Optional[str] = None,
                        data: DataT = None,
                        status_code: int = HTTPStatus.OK) -> Response:
        base_response = cls(success=success, message=message, code=code, data=data)
        return Response(response=base_response.json(exclude_none=True, ensure_ascii=False), status=status_code,
                        mimetype='application/json; charset=utf-8')

    @classmethod
    def create_no_content_response(cls) -> Response:
        return Response(status=HTTPStatus.NO_CONTENT)

    @classmethod
    def get_base_response(cls, response: Response) -> BaseResponse[Any]:
        if 300 > response.status_code >= 200:
            return BaseResponse[Any](**response.json())

        failed_response: BaseResponse[Any] = BaseResponse(success=False,
                                                          code=str(response.status_code),
                                                          message=response.text)

        logger.warning(f'Failed response received: {failed_response}')

        return failed_response
