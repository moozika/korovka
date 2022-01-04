from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from v1.api import v1_router
from v2.api import v2_router


app = FastAPI()

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
