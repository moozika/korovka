from typing import Optional
from odmantic import Model, Reference
from typing import List
import datetime
# import bson


class User(Model):
    email: str
    logins: int
    created_date: str = str(datetime.datetime.now())
    last_login_date: str = str(datetime.datetime.now())
    spotify_id: str
    display_name: str
    profile_pic_url: str
    moods: List[str]
    liked: List[str]


class Mood(Model):
    name: str
    description: str
    likes: int
    vibes: List[str]
    main_song: Optional[str] = ''
    songs: List[str]
    created_date: str = str(datetime.datetime.now())
    author: User = Reference()
    playlist_id: Optional[str] = ''
