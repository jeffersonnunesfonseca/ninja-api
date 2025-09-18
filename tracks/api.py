from typing import List, Optional

from http import HTTPStatus
from django.http import HttpRequest

from ninja import NinjaAPI

from tracks.models import Track
from tracks.schema import TrackSchema, NotFoundSchema

api = NinjaAPI()

@api.get('/_health')
def health(request: HttpRequest):
    return "OK"


@api.get('/tracks', response=List[TrackSchema])
def tracks(request: HttpRequest, title: Optional[str] = None):
    if title:
        return Track.objects.filter(title__icontains=title)
    return Track.objects.all()

@api.get('/tracks/{track_id}', response={HTTPStatus.OK: TrackSchema, HTTPStatus.NOT_FOUND: NotFoundSchema})
def tracks_by_id(request: HttpRequest, track_id: int):
    # return Track.objects.all()
    try:
        return Track.objects.get(pk=track_id)
    except Track.DoesNotExist as e:
        return HTTPStatus.NOT_FOUND, {"message": "Track does not exists"}

@api.post('/tracks', response={HTTPStatus.CREATED: TrackSchema})
def create_track(request: HttpRequest, track: TrackSchema):
    return Track.objects.create(**track.dict())