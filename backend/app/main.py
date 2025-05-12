from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import AsyncDBSessionMiddleware
from app import settings  # an object to provide global access to a database session
from app.api.trips import router as trips_router
from app.api.special_lists import router as special_lists_router

origins = [
    "http://localhost:3000",
]


app = FastAPI()
app.add_middleware(
    AsyncDBSessionMiddleware, 
    commit_on_exit=True,
    db_url=settings.POSTGRES_URL
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trips_router)
app.include_router(special_lists_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
