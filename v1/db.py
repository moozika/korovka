import os
# db library imports
from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient

# environment variables for mongo
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PWD = os.getenv("MONGODB_PWD")
MONGODB_URL_PRE = os.getenv("MONGODB_URL_PRE")
MONGODB_ENV = os.getenv("MONGODB_ENV") if os.getenv("MONGODB_ENV") else "dev"


client = AsyncIOMotorClient(
    "mongodb+srv://{}:{}@{}{}/moozika_{}?retryWrites=true&w=majority".format(
        MONGODB_USERNAME,
        MONGODB_PWD,
        MONGODB_URL_PRE,
        ".mongodb.net",
        MONGODB_ENV
    )
)
engine = AIOEngine(motor_client=client, database=f'moozika_{MONGODB_ENV}')

token_to_id = dict()
blacklist_token = set()

vibes_dict = {
    'Uplifting': ['yellow-100', 'yellow-300'],
    'Romantic': ['red-200', 'red-400'],
    'Calm': ['blue-200', 'blue-400'],
    'Fresh': ['green-300', 'green-500'],
    'Eclectic': ['purple-300', 'purple-500'],
    'Energetic': ['orange-400', 'orange-600']
}
vibes = [{'name': k, 'colors': v} for k, v in vibes_dict.items()]
