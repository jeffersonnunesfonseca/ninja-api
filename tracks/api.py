from http import HTTPStatus

from django.http import HttpRequest
from ninja import NinjaAPI

from tracks.models import Track
from tracks.schema import (
    BaseResponse,
    NotFoundSchema,
    TrackSchema,
    TrackSchemaResponse,
    base_response,
)

api = NinjaAPI()


@api.get("/_health")
def health(request: HttpRequest):
    return "OK"


@api.get("/", response=BaseResponse[list[TrackSchemaResponse]])
@base_response
def tracks(request: HttpRequest, title: str | None = None):
    if title:
        return Track.objects.filter(title__icontains=title)
    return Track.objects.all()


@api.get(
    "/{track_id}",
    response={
        HTTPStatus.OK: BaseResponse[TrackSchemaResponse],
        HTTPStatus.NOT_FOUND: BaseResponse[NotFoundSchema],
    },
)
@base_response
def tracks_by_id(request: HttpRequest, track_id: int):
    return Track.objects.get(pk=track_id)


@api.post("/", response={HTTPStatus.CREATED: BaseResponse[TrackSchemaResponse]})
@base_response
def create_track(request: HttpRequest, track: TrackSchema):
    return HTTPStatus.CREATED, Track.objects.create(**track.dict())


@api.put(
    "/{track_id}",
    response={
        HTTPStatus.OK: BaseResponse[TrackSchemaResponse],
        HTTPStatus.NOT_FOUND: BaseResponse[NotFoundSchema],
    },
)
@base_response
def update_track(request: HttpRequest, track_id: int, data: TrackSchema):
    track = Track.objects.get(pk=track_id)
    for attr, value in data.dict().items():
        setattr(track, attr, value)

    track.save()
    return track


@api.delete(
    "/{track_id}",
    response={HTTPStatus.OK: None, HTTPStatus.NOT_FOUND: BaseResponse[NotFoundSchema]},
)
@base_response
def delete_track(request: HttpRequest, track_id: int):
    track = Track.objects.get(pk=track_id)
    track.delete()
    return HTTPStatus.OK
