from datetime import datetime
from enum import Enum
from functools import wraps
from http import HTTPStatus
from typing import Generic, Optional, TypeVar

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from ninja import Schema
from ninja.errors import ValidationError

T = TypeVar("T")


class BaseResponseStatus(str, Enum):
    ERROR = "error"
    SUCCESS = "success"


class BaseResponse(Schema, Generic[T]):
    status: BaseResponseStatus
    message: str
    data: Optional[T] = None


class TrackSchema(Schema):
    title: str
    artist: str
    duration: float
    last_play: datetime


class TrackSchemaResponse(TrackSchema):
    id: int


class NotFoundSchema(Schema):
    message: str


HTTP_MAP = {
    ObjectDoesNotExist: HTTPStatus.NOT_FOUND,
    PermissionDenied: HTTPStatus.FORBIDDEN,
    ValidationError: HTTPStatus.UNPROCESSABLE_ENTITY,
    ValueError: HTTPStatus.BAD_REQUEST,
}


def base_response(func):
    """
    Mantem o padrão de retorno  'BaseResponse' de forma que não afeta o openapi
    O BaseRender e Middleware não dão certo pois o pydantic força a validação
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            result = func(request, *args, **kwargs)

            status_code, message, data = HTTPStatus.OK, "OK", result

            # Se o endpoint já retornou (status, message, data), respeita isso
            if isinstance(result, tuple) and len(result) == 3:
                status_code, message, data = result
            elif isinstance(result, tuple) and len(result) == 2:
                # Caso só (status, data)
                status_code, data = result
                message = HTTPStatus(status_code).phrase

            response = BaseResponse(
                status=BaseResponseStatus.SUCCESS,
                message=message,
                data=data if status_code != HTTPStatus.NO_CONTENT else None,
            )
            return status_code, response.dict()

        except Exception as e:
            # Verifica se a exceção está no mapa
            for exc_type, http_code in HTTP_MAP.items():
                if isinstance(e, exc_type):  # pega subclasses (ex: Track.DoesNotExist)
                    response = BaseResponse(
                        status=BaseResponseStatus.ERROR,
                        message=str(e) or http_code.phrase,
                        data=None,
                    )
                    return http_code, response.dict()

            # fallback erro 500
            response = BaseResponse(
                status=BaseResponseStatus.ERROR,
                message=str(e) or "Internal Server Error",
                data=None,
            )
            return HTTPStatus.INTERNAL_SERVER_ERROR, response.dict()

    return wrapper
