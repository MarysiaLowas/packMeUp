import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import AsyncDBSessionMiddleware
from app import settings  # an object to provide global access to a database session
from app.api.trips import router as trips_router
from app.api.special_lists import router as special_lists_router
from app.api.generated_lists import router as generated_lists_router
from app.api import auth

# Configure root logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Create logger for this module
logger = logging.getLogger(__name__)

origins = [
    "http://localhost:3000",
    "http://localhost:4321",  # Astro's default port
    "http://127.0.0.1:4321",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:4322",
    "http://127.0.0.1:4310",
]

app = FastAPI(
    title="PackMeUp API",
    description="API for managing packing lists and trips",
    version="1.0.0"
)

# Add middleware first
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

app.add_middleware(
    AsyncDBSessionMiddleware, 
    commit_on_exit=True,
    db_url=settings.POSTGRES_URL
)

# Then add routers
app.include_router(trips_router)
app.include_router(special_lists_router)
app.include_router(generated_lists_router)
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("")
async def root():
    return {"message": "PackMeUp API"}
