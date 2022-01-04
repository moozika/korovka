from fastapi import APIRouter
from .main import v1_app

v1_router = APIRouter()
v1_router.include_router(v1_app, tags=['sussy'])
# v1_router.include_router(login.router, tags=["login"])
# v1_router.include_router(users.router, prefix="/users", tags=["users"])
# v1_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# v1_router.include_router(items.router, prefix="/items", tags=["items"])