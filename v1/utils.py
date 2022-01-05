from fastapi import HTTPException
import requests
from v1.models import Mood
from v1.db import engine
from v1.models import User


def get_email(cache: dict, token: str) -> str:
    if token in cache.keys():
        return cache[token]
    else:
        resp = requests.get(
            "https://api.spotify.com/v1/me",
            headers={
                'Authorization': "Bearer " + token
            }
        )
        if resp.status_code != 200:
            print(resp.json())
            raise HTTPException(
                status_code=401,
                detail={
                    "error": "Spotify Authorization Failed", 
                    'spotify_api_msg': resp.json()['error']['message']
                }
            )
        cache[token] = resp.json()['email']
        return cache[token]


async def get_user(email: str) -> User:
    if email is None:
        raise HTTPException(
            status_code=400,
            detail='Failed to get user id from cache'
        )
    curr_user = await engine.find_one(User, User.email == email)
    if curr_user is None:
        raise HTTPException(
            status_code=400,
            detail='Failed to find account with given email'
        )
    else:
        return curr_user


def verify_mood_owner(mood: Mood, user: User, mood_id: int):
    if mood is None:
        raise HTTPException(
            status_code=404,
            detail='Mood with id ' + mood_id + ' not found.'
        )
    if mood.author.email != user.email:
        raise HTTPException(
            status_code=405,
            detail='User does not have permission to delete this mood.'
        )
