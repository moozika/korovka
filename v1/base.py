# fastapi imports
from fastapi import Header, HTTPException, APIRouter
# models and utils imports
from v1.models import User, Mood
from v1.schemas import Dashboard, DashboardMood
from v1.utils import get_email
from v1.db import token_to_id, engine, vibes
# std imports
import datetime
import requests
import bson

base_router = APIRouter()


@base_router.get("/status")
async def status():
    return {
        'status': 'success'
    }


@base_router.post("/user", response_model=User)
async def init_user(
    access_token: str = Header(None, convert_underscores=False)
):
    print("Access token:" + access_token)
    resp = requests.get(
        "https://api.spotify.com/v1/me",
        headers={
            'Authorization': "Bearer " + access_token
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
    user_json = resp.json()
    curr_user = await engine.find_one(User, User.email == user_json['email'])
    if curr_user is not None:
        print("User already exists, incrementing logins")
        curr_user.logins += 1
        curr_user.last_login_date = datetime.datetime.utcnow().isoformat()
        if 'images' in user_json.keys():
            curr_user.profile_pic_url = user_json['images'][0]['url']
        else:
            curr_user.profile_pic_url = ''
        curr_user.display_name = user_json['display_name']
        await engine.save(curr_user)
        token_to_id[access_token] = curr_user.email
        return curr_user
    pp_url = user_json['images'][0]['url'] if user_json['images'] else ''
    new_user = User(
        email=user_json['email'],
        logins=1,
        created_date=datetime.datetime.utcnow().isoformat(),
        last_login_date=datetime.datetime.utcnow().isoformat(),
        profile_pic_url=pp_url,
        display_name=user_json['display_name'],
        spotify_id=user_json['id'],
        liked=[],
        moods=[]
    )
    await engine.save(new_user)
    token_to_id[access_token] = new_user.email
    print("Created new user")
    return new_user


@base_router.get('/dashboard', response_model=Dashboard)
async def dashboard(
    access_token: str = Header(None, convert_underscores=False)
):
    user_email = get_email(token_to_id, access_token)
    if user_email is None:
        raise HTTPException(
            status_code=400,
            detail='Failed to get user id from cache'
        )
    user = await engine.find_one(User, User.email == user_email)
    user_moods = [
        await engine.find_one(
            Mood,
            Mood.id == bson.ObjectId(mood)
        ) for mood in user.moods
    ]
    liked_moods = [
        await engine.find_one(
            Mood,
            Mood.id == bson.ObjectId(mood)
        ) for mood in user.liked
    ]
    dashboard = Dashboard(
        user_email=user.email,
        moodz=[
            DashboardMood(
                id=str(m.id),
                name=m.name,
                created_on=m.created_date,
                likes=m.likes,
                liked=str(m.id) in user.liked,
                vibes=[{'name': m, 'colors': vibes[m]} for m in m.vibes],
                songs=m.songs,
                num_songs=len(m.songs),
                description=m.description
            ) for m in user_moods],
        liked_moodz=[
            DashboardMood(
                id=str(m.id),
                name=m.name,
                created_on=m.created_date,
                likes=m.likes,
                num_songs=len(m.songs),
                liked=str(m.id) in user.liked,
                vibes=[{'name': m, 'colors': vibes[m]} for m in m.vibes],
                description=m.description
            ) for m in liked_moods
        ]
    )
    return dashboard


@base_router.get('/vibes')
async def get_vibes(
    access_token: str = Header(None, convert_underscores=False)
):
    if access_token is None:
        return vibes


@base_router.post('/vibes')
async def create_vibe(
    access_token: str = Header(None, convert_underscores=False)
):
    return {}
