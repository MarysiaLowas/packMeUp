import os
import sys
import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.models import Base


# Test database URL - this will be an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def anyio_backend():
    """Return the anyio backend for pytest-asyncio."""
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_engine():
    """Create a new async engine for testing."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
async def async_session(async_engine):
    """Create a new async session for testing."""
    async_session_maker = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest.fixture
def test_client():
    """Create a test client for FastAPI."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_db_session(mocker):
    """Mock the database session dependency."""
    mock_session = mocker.MagicMock()
    
    # Patch the get_db dependency in your app to use the mock session
    mocker.patch("app.main.get_db", return_value=mock_session)
    
    return mock_session


# Add more fixtures as needed for your specific application requirements 