import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
import json
from app.main import app

# Sample integration test for the API
# Replace with actual tests for your application's endpoints

@pytest.mark.integration
class TestAPIEndpoints:
    """Test class for API integration tests."""
    
    def test_health_check(self, test_client):
        """Test the health check endpoint."""
        # This test assumes you have a /health endpoint
        # Adjust according to your actual API
        response = test_client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
    
    @pytest.mark.asyncio
    async def test_async_endpoint(self, async_session):
        """Test an endpoint using async client."""
        # This test demonstrates using an async client with FastAPI
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}
    
    def test_create_resource(self, test_client, mock_db_session):
        """Test creating a resource via the API."""
        # Setup mock to return appropriate data when called
        mock_db_session.add.return_value = None
        mock_db_session.commit.return_value = None
        mock_db_session.refresh.return_value = None
        
        # Sample payload - adjust according to your API
        payload = {
            "name": "Test Resource",
            "description": "A test resource"
        }
        
        # Make the request
        response = test_client.post(
            "/resources/",
            json=payload
        )
        
        # Assertions
        assert response.status_code == 201
        
        # Verify mock was called
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
    
    @pytest.mark.parametrize(
        "resource_id,expected_status",
        [
            (1, 200),
            (999, 404),
        ],
    )
    def test_get_resource(self, test_client, resource_id, expected_status):
        """Test getting a resource by ID."""
        response = test_client.get(f"/resources/{resource_id}")
        assert response.status_code == expected_status 