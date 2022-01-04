# fastapi imports
from fastapi import Header, HTTPException, APIRouter
# std imports
import requests

songs_router = APIRouter()


@songs_router.get("/search")
async def search_songs(
    query: str,
    access_token: str = Header(None, convert_underscores=False)
):
    search_resp = requests.get(
        'https://api.spotify.com/v1/search',
        params={'type': 'track', 'q': query, 'limit': 5},
        headers={
            'Authorization': "Bearer " + access_token
        }
    )
    if search_resp.status_code != 200:
        raise HTTPException(status_code=404, detail="Failed API calls")
    songs = []
    for s in search_resp.json()['tracks']['items']:
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


@songs_router.get('/{id}')
async def get_song_by_id(
    id: str,
    access_token: str = Header(None, convert_underscores=False)
):
    song_resp = requests.get(
        'https://api.spotify.com/v1/tracks/{}'.format(id),
        headers={
            'Authorization': "Bearer " + access_token
        }
    )
    if song_resp.status_code != 200:
        raise HTTPException(status_code=404, detail="Failed API calls")
    song_json = song_resp.json()
    song = {
        'name': song_json['name'],
        'id': id,
        'album': song_json['album']['name'],
        'artists': ", ".join([a['name'] for a in song_json['artists']])
    }
    for i in song_json['album']['images']:
        if i['height'] == 64:
            song['image_url'] = i['url']
    return song
