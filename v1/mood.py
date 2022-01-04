# fastapi imports
from fastapi import Header, HTTPException, APIRouter
# models and utils imports
from v1.models import DisplayMood
from v1.models import User, Mood, MoodBody
from v1.utils import get_email
from v1.db import engine, token_to_id
# std imports
import requests
import bson

mood_router = APIRouter()


@mood_router.post('/mood')
async def create_mood(
    mood: MoodBody,
    access_token: str = Header(None, convert_underscores=False)
):
    user_email = get_email(token_to_id, access_token)
    if user_email is None:
        raise HTTPException(
            status_code=400,
            detail='Failed to get user id from cache'
        )
    curr_user = await engine.find_one(User, User.email == user_email)
    new_mood = Mood(
        likes=1,
        author=curr_user,
        vibes=mood.vibes,
        name=mood.name,
        description=mood.description,
        songs=mood.songs
    )
    await engine.save(new_mood)
    curr_user.moods.append(str(new_mood.id))
    curr_user.liked.insert(0, str(new_mood.id))
    await engine.save(curr_user)
    return new_mood


@mood_router.post('/{mood_id}/edit')
async def edit_mood(
    mood_id: str,
    update: MoodBody,
    access_token: str = Header(None, convert_underscores=False)
):
    user_email = get_email(token_to_id, access_token)
    if user_email is None:
        raise HTTPException(
            status_code=400,
            detail='Failed to get user id from cache'
        )
    curr_user = await engine.find_one(User, User.email == user_email)
    mood = await engine.find_one(Mood, Mood.id == bson.ObjectId(mood_id))
    if mood is None:
        raise HTTPException(
            status_code=404,
            detail='Mood with id ' + mood_id + 'not found.'
        )
    if mood.author.email != curr_user.email:
        raise HTTPException(
            status_code=405,
            detail='User does not have permission to edit this mood.'
        )
    mood.description = update.description
    mood.name = update.name
    mood.vibes = update.vibes
    mood.songs = update.songs
    await engine.save(mood)
    curr_user.moods.remove(mood_id)
    curr_user.moods.insert(0, str(mood.id))
    return {'status': 'success'}


@mood_router.delete('/{mood_id}')
async def delete_mood(
    mood_id: str,
    access_token: str = Header(None, convert_underscores=False)
):
    user_email = get_email(token_to_id, access_token)
    if user_email is None:
        raise HTTPException(
            status_code=400,
            detail='Failed to get user id from cache'
        )
    curr_user = await engine.find_one(User, User.email == user_email)
    mood = await engine.find_one(Mood, Mood.id == bson.ObjectId(mood_id))
    if mood is None:
        raise HTTPException(
            status_code=404,
            detail='Mood with id ' + mood_id + 'not found.'
        )
    if mood.author != curr_user:
        raise HTTPException(
            status_code=405,
            detail='User does not have permission to delete this mood.'
        )
    curr_user.moods.remove(mood_id)
    try:
        curr_user.liked.remove(mood_id)
    except ValueError:
        print("User did not like the post in the first place!")
    await engine.delete(mood)
    await engine.save(curr_user)
    return {'status': 'Deleted successfully'}


@mood_router.get('/{mood_id}', response_model=DisplayMood)
async def get_mood(mood_id: str):
    mood = await engine.find_one(Mood, Mood.id == bson.ObjectId(mood_id))
    if mood is None:
        raise HTTPException(
            status_code=404,
            detail='Mood with id {} not found.'.format(mood_id)
        )
    m = DisplayMood(
        id=str(mood.id),
        name=mood.name,
        created_on=mood.created_date,
        likes=mood.likes,
        # liked=str(mood.id) in user.liked,
        vibes=[{'name': m, 'colors': mood.vibes[m]} for m in mood.vibes],
        songs=mood.songs,
        description=mood.description,
        author=mood.author.display_name,
        img_url=mood.author.profile_pic_url
    )
    return m


@mood_router.get('/{mood_id}/recommendations')
async def get_mood_recommendations(
    mood_id: str,
    access_token: str = Header(None, convert_underscores=False)
):
    user_email = get_email(token_to_id, access_token)
    if user_email is None:
        raise HTTPException(
            status_code=400,
            detail='Failed to get user id from cache'
        )
    curr_user = await engine.find_one(User, User.email == user_email)
    mood = await engine.find_one(Mood, Mood.id == bson.ObjectId(mood_id))
    if mood is None:
        raise HTTPException(
            status_code=404,
            detail='Mood with id ' + mood_id + ' not found.'
        )
    if mood.author.email != curr_user.email:
        raise HTTPException(
            status_code=405,
            detail='User does not have permission to delete this mood.'
        )
    s_tracks = mood.songs[:5]
    reqs_resp = requests.get(
        'https://api.spotify.com/v1/recommendations',
        params={
            'limit': 10,
            'seed_tracks': ",".join(s_tracks)
        },
        headers={
            'Authorization': "Bearer " + access_token
        }
    )
    songs = []
    for s in reqs_resp.json()['tracks']:
        new_song = {}
        new_song['name'] = s['name']
        new_song['id'] = s['id']
        new_song['album'] = s['album']['name']
        new_song['artists'] = ", ".join([a['name'] for a in s['artists']])
        for i in s['album']['images']:
            if i['height'] == 64:
                new_song['image_url'] = i['url']
        songs.append(new_song)
    return songs


@mood_router.get('/{mood_id}/like')
async def like_mood(
    mood_id: str,
    access_token: str = Header(None, convert_underscores=False)
):
    user_email = get_email(token_to_id, access_token)
    if user_email is None:
        raise HTTPException(
            status_code=400,
            detail='Failed to get user id from cache'
        )
    curr_user = await engine.find_one(User, User.email == user_email)
    mood = await engine.find_one(Mood, Mood.id == bson.ObjectId(mood_id))
    if mood is None:
        raise HTTPException(
            status_code=404,
            detail='Mood with id ' + mood_id + ' not found.'
        )
    if str(mood.id) in curr_user.liked:
        mood.likes -= 1
        curr_user.liked.remove(str(mood.id))
    else:
        mood.likes += 1
        curr_user.liked.insert(0, str(mood.id))
    await engine.save_all([mood, curr_user])
    return {'status': 'completed'}


@mood_router.post('/{mood_id}/song/{song_id}')
async def add_song_to_mood(
    mood_id: str,
    song_id: str,
    access_token: str = Header(None, convert_underscores=False)
):
    user_email = get_email(token_to_id, access_token)
    if user_email is None:
        raise HTTPException(
            status_code=400,
            detail='Failed to get user id from cache'
        )
    curr_user = await engine.find_one(User, User.email == user_email)
    mood = await engine.find_one(Mood, Mood.id == bson.ObjectId(mood_id))
    if mood is None:
        raise HTTPException(
            status_code=404,
            detail='Mood with id ' + mood_id + ' not found.'
        )
    if mood.author.email != curr_user.email:
        raise HTTPException(
            status_code=405,
            detail='User does not have permission to delete this mood.'
        )
    mood.songs.append(song_id)
    await engine.save(mood)
    return {'status': 'completed'}


@mood_router.delete('/{mood_id}/song/{song_id}')
async def delete_song_from_mood(
    mood_id: str,
    song_id: str,
    access_token: str = Header(None, convert_underscores=False)
):
    user_email = get_email(token_to_id, access_token)
    if user_email is None:
        raise HTTPException(
            status_code=400,
            detail='Failed to get user id from cache'
        )
    curr_user = await engine.find_one(User, User.email == user_email)
    mood = await engine.find_one(Mood, Mood.id == bson.ObjectId(mood_id))
    if mood is None:
        raise HTTPException(
            status_code=404,
            detail='Mood with id ' + mood_id + ' not found.'
        )
    if mood.author.email != curr_user.email:
        raise HTTPException(
            status_code=405,
            detail='User does not have permission to delete this mood.'
        )
    mood.songs.remove(song_id)
    await engine.save(mood)
    return {'status': 'completed'}


@mood_router.post('/{mood_id}/set_main_song/{song_id}')
async def set_main_song(
    mood_id: str,
    song_id: str,
    access_token: str = Header(None, convert_underscores=False)
):
    user_email = get_email(token_to_id, access_token)
    if user_email is None:
        raise HTTPException(
            status_code=400,
            detail='Failed to get user id from cache'
        )
    curr_user = await engine.find_one(User, User.email == user_email)
    mood = await engine.find_one(Mood, Mood.id == bson.ObjectId(mood_id))
    if mood is None:
        raise HTTPException(
            status_code=404,
            detail='Mood with id ' + mood_id + ' not found.'
        )
    if mood.author.email != curr_user.email:
        raise HTTPException(
            status_code=405,
            detail='User does not have permission to delete this mood.'
        )
    if song_id not in mood.songs:
        return {'message': 'Song id is not in given mood\'s songs'}, 205
    if mood.main_song == '':
        mood.main_song = song_id
    else:
        mood.main_song = song_id
    engine.save(mood)
    return {'added': song_id}
