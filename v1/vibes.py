from fastapi import Header, APIRouter
from v1.models import Vibe
from v1.db import vibes, token_to_id, engine
from v1.utils import get_email, get_user
from typing import List

router = APIRouter()


@router.get('')
async def get_vibes(
    access_token: str = Header(None, convert_underscores=False)
):
    if access_token is None:
        return vibes
    else:
        curr_user = await get_user(get_email(token_to_id, access_token))
        return vibes + curr_user.vibes


@router.post('')
async def create_vibes(
    vibes: List[Vibe],
    access_token: str = Header(None, convert_underscores=False)
):
    curr_user = await get_user(get_email(token_to_id, access_token))
    curr_user.vibes.extend(vibes)
    await engine.save(curr_user)
    return {
        'status': 'success'
    }
