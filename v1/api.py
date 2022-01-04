from fastapi import APIRouter
from .songs import songs_router
from .mood import mood_router
from .base import base_router


v1_router = APIRouter()

v1_router.include_router(songs_router, prefix='/songs', tags=['songs'])
v1_router.include_router(mood_router, prefix='/mood', tags=['mood'])
v1_router.include_router(base_router, tags=['base'])
