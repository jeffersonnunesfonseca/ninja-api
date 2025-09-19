from datetime import datetime
from enum import Enum
from typing import Generic, Optional, TypeVar

from ninja import Schema

T = TypeVar("T")


class BaseResponseStatus(Enum):
    ERROR = "error"
    SUCCESS = "success"


# ninja suporta generics type
class BaseResponse(Schema, Generic[T]):
    status: BaseResponseStatus
    message: str
    data: Optional[T] = None
    error: Optional[dict] = None


class TrackSchema(Schema):
    title: str
    artist: str
    duration: float
    last_play: datetime


class TrackSchemaResponse(TrackSchema):
    id: int


class NotFoundSchema(Schema):
    message: str
