from fastapi import Header, APIRouter
from v1.db import vibes, token_to_id
from v1.utils import get_email, get_user

router = APIRouter()


@router.get('/')
async def get_vibes(
    access_token: str = Header(None, convert_underscores=False)
):
    if access_token is None:
        return vibes


@router.post('/')
async def create_vibe(
    access_token: str = Header(None, convert_underscores=False)
):
    curr_user = await get_user(get_email(token_to_id, access_token))
    return {}
