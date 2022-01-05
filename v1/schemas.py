from typing import Optional
from v1.models import Vibe
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime


class MoodBody(BaseModel):
    name: str
    vibes: List[Vibe]
    songs: List[str]
    description: str


class DashboardMood(BaseModel):
    id: str
    name: str
    likes: int
    liked: Optional[bool]
    created_on: str = str(datetime.datetime.now())
    vibes: List[Dict[str, Any]]
    songs: Optional[List[str]]
    description: str


class DisplayMood(BaseModel):
    id: str
    name: str
    likes: int
    liked: Optional[bool]
    created_on: str = str(datetime.datetime.now())
    vibes: List[Vibe]
    songs: Optional[List[str]]
    description: str
    author: str
    img_url: str


class Dashboard(BaseModel):
    user_email: str
    moodz: List[DashboardMood]
    liked_moodz: List[DashboardMood]


class PlaylistBody(BaseModel):
    name: str
    public: bool
    collaborative: bool
    description: str
