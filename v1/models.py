from typing import Optional
from odmantic import Model, EmbeddedModel, Reference
from typing import List
import datetime


class Vibe(EmbeddedModel):
    name: str
    colors: List[str]


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
    vibes: List[Vibe] = []


class Mood(Model):
    name: str
    description: str
    likes: int
    vibes: List[Vibe]
    main_song: Optional[str] = ''
    songs: List[str]
    created_date: str = str(datetime.datetime.now())
    author: User = Reference()
    playlist_id: Optional[str] = ''
