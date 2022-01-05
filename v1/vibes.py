from fastapi import Header, APIRouter
from v1.db import vibes

router = APIRouter()


@router.get('/vibes')
async def get_vibes(
    access_token: str = Header(None, convert_underscores=False)
):
    if access_token is None:
        return vibes


@router.post('/vibes')
async def create_vibe(
    access_token: str = Header(None, convert_underscores=False)
):
    return {}
