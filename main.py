from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from v1.api import v1_router
from v2.api import v2_router
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_restful.tasks import repeat_every
from v1.db import token_to_id, blacklist_token

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000)

origins = [
    "http://localhost:3000",
    "https://moozika.herokuapp.com",
    "https://moozika.netlify.app",
    "http://moozika.io",
    "https://moozika.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(v1_router, prefix="/api/v1", tags=['v1'])
app.include_router(v2_router, prefix="/api/v2", tags=['v2'])


@app.get('/')
async def root():
    return {
        'status': 'available'
    }


@app.on_event("startup")
@repeat_every(seconds=60*60)
def remove_expired_tokens():
    print('running')
    for token, obj in token_to_id.items:
        print(obj)
    for token, dt in blacklist_token:
        print(dt)

# TODO: finish token cache cleaning