from typing import List, Optional

from http import HTTPStatus
from django.http import HttpRequest

from ninja import NinjaAPI

from tracks.models import Track
from tracks.schema import TrackSchema, TrackSchemaResponse, NotFoundSchema

api = NinjaAPI()

@api.get('/_health')
def health(request: HttpRequest):
    return "OK"


@api.get('/tracks', response=List[TrackSchemaResponse])
def tracks(request: HttpRequest, title: Optional[str] = None):
    if title:
        return Track.objects.filter(title__icontains=title)
    return Track.objects.all()

@api.get('/tracks/{track_id}', response={HTTPStatus.OK: TrackSchemaResponse, HTTPStatus.NOT_FOUND: NotFoundSchema})
def tracks_by_id(request: HttpRequest, track_id: int):
    try:
        return Track.objects.get(pk=track_id)
    except Track.DoesNotExist as e:
        return HTTPStatus.NOT_FOUND, {"message": "Track does not exists"}

@api.post('/tracks', response={HTTPStatus.CREATED: TrackSchemaResponse})
def create_track(request: HttpRequest, track: TrackSchema):
    return Track.objects.create(**track.dict())


@api.put('/tracks/{track_id}', response={HTTPStatus.OK: TrackSchemaResponse, HTTPStatus.NOT_FOUND: NotFoundSchema})
def update_track(request: HttpRequest, track_id: int, data: TrackSchema):
    try:
        track =  Track.objects.get(pk=track_id)
        for attr, value in data.dict().items():
            setattr(track, attr, value)
        
        track.save()
        return HTTPStatus.OK, track
    except Track.DoesNotExist as e:
        return HTTPStatus.NOT_FOUND, {"message": "Track does not exists"}
    

@api.delete('/tracks/{track_id}', response={HTTPStatus.OK: None, HTTPStatus.NOT_FOUND: NotFoundSchema})
def delete_track(request: HttpRequest, track_id: int):
    try:
        track =  Track.objects.get(pk=track_id)
        track.delete()
        return HTTPStatus.OK
    except Track.DoesNotExist as e:
        return HTTPStatus.NOT_FOUND, {"message": "Track does not exists"}
