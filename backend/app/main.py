import logging

from dotenv import load_dotenv

# Path to your .env file (one directory up from backend, in the project root)
# This assumes your script's CWD when running is the 'backend' directory.
dotenv_path = "../.env"
# You could also use an absolute path:
# dotenv_path = "/home/marysia/Opos/10xdev/pack_me_up/.env"

# Load environment variables from .env file
# Pass override=True if you want .env to take precedence over existing system env vars
load_dotenv(dotenv_path=dotenv_path, override=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import AsyncDBSessionMiddleware  # type: ignore

from app import settings  # an object to provide global access to a database session
from app.api import auth
from app.api.generated_lists import router as generated_lists_router
from app.api.special_lists import router as special_lists_router
from app.api.trips import router as trips_router
from app.config import CORS_ORIGINS

# Configure root logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

# Create logger for this module
logger = logging.getLogger(__name__)

# Development settings
DEV_MODE = True  # TODO: Move to environment variable

app = FastAPI(
    title="PackMeUp API",
    description="API for managing packing lists and trips",
    version="1.0.0",
)

# Add middleware first
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.add_middleware(
    AsyncDBSessionMiddleware, commit_on_exit=True, db_url=settings.POSTGRES_URL
)

# Then add routers
app.include_router(trips_router)
app.include_router(special_lists_router)
app.include_router(generated_lists_router)
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])


@app.get("")
async def root():
    return {"message": "PackMeUp API"}
