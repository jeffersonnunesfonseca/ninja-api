from http import HTTPStatus
from typing import List, Optional

import orjson
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer

from tracks.models import Track
from tracks.schema import BaseResponse, NotFoundSchema, TrackSchema, TrackSchemaResponse

from .schema import BaseResponseStatus


class CustomRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request: HttpRequest, data, *, response_status: int):
        # Monta o formato padrão de resposta
        body = {
            "status": (
                BaseResponseStatus.SUCCESS.value
                if response_status < 400
                else BaseResponseStatus.ERROR.value
            ),
            "message": "OK" if response_status < 400 else "Erro na requisição",
            "data": data if response_status < 400 else None,
            "error": data if response_status >= 400 else None,
        }
        return orjson.dumps(body)


api = NinjaAPI(renderer=CustomRenderer())


@api.get("/_health")
def health(request: HttpRequest):
    return "OK"


@api.get("/tracks", response=BaseResponse[List[TrackSchemaResponse]])
def tracks(request: HttpRequest, title: Optional[str] = None):
    if title:
        return Track.objects.filter(title__icontains=title)
    return Track.objects.all()


@api.get(
    "/tracks/{track_id}",
    response={HTTPStatus.OK: TrackSchemaResponse, HTTPStatus.NOT_FOUND: NotFoundSchema},
)
def tracks_by_id(request: HttpRequest, track_id: int):
    try:
        return Track.objects.get(pk=track_id)
    except Track.DoesNotExist:
        return HTTPStatus.NOT_FOUND, {"message": "Track does not exists"}


@api.post("/tracks", response={HTTPStatus.CREATED: TrackSchemaResponse})
def create_track(request: HttpRequest, track: TrackSchema):
    return Track.objects.create(**track.dict())


@api.put(
    "/tracks/{track_id}",
    response={HTTPStatus.OK: TrackSchemaResponse, HTTPStatus.NOT_FOUND: NotFoundSchema},
)
def update_track(request: HttpRequest, track_id: int, data: TrackSchema):
    try:
        track = Track.objects.get(pk=track_id)
        for attr, value in data.dict().items():
            setattr(track, attr, value)

        track.save()
        return HTTPStatus.OK, track
    except Track.DoesNotExist:
        return HTTPStatus.NOT_FOUND, {"message": "Track does not exists"}


@api.delete(
    "/tracks/{track_id}",
    response={HTTPStatus.OK: None, HTTPStatus.NOT_FOUND: NotFoundSchema},
)
def delete_track(request: HttpRequest, track_id: int):
    try:
        track = Track.objects.get(pk=track_id)
        track.delete()
        return HTTPStatus.OK
    except Track.DoesNotExist:
        return HTTPStatus.NOT_FOUND, {"message": "Track does not exists"}
