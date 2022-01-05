from fastapi import APIRouter
from v1 import songs, mood, base, vibes
from fastapi_restful.tasks import repeat_every
from korovka.main import app
from v1.db import token_to_id, blacklist_token

v1_router = APIRouter()


v1_router.include_router(songs.router, prefix='/songs', tags=['v1_songs'])
v1_router.include_router(mood.router, prefix='/mood', tags=['v1_mood'])
v1_router.include_router(vibes.router, prefix='/vibes', tags=['v1_vibes'])
v1_router.include_router(base.router, tags=['v1_base'])


@app.on_event("startup")
@repeat_every(seconds=60*60)
def remove_expired_tokens():
    for token, obj in token_to_id.items:
        print(obj)
    for token, dt in blacklist_token:
        print(dt)
