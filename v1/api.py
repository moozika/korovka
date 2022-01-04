from fastapi import APIRouter
from v1 import songs, mood, base


v1_router = APIRouter()

v1_router.include_router(songs.router, prefix='/songs', tags=['v1_songs'])
v1_router.include_router(mood.router, prefix='/mood', tags=['v1_mood'])
v1_router.include_router(base.router, tags=['v1_base'])
