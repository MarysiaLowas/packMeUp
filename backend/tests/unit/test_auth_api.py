import uuid
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from app.main import app
from app.models import User
from app.services.auth_service import Token

# Test constants
TEST_USER_ID = uuid.uuid4()
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "StrongPass123"
TEST_FIRST_NAME = "Test"


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def mock_user():
    user = AsyncMock(spec=User)
    user.id = TEST_USER_ID
    user.email = TEST_EMAIL
    user.first_name = TEST_FIRST_NAME
    return user


@pytest.fixture
def mock_token():
    return Token(
        access_token="test_access_token",
        token_type="bearer",
        expires_in=1800,
        refresh_token="test_refresh_token",
    )


class TestAuthApi:
    @pytest.mark.parametrize(
        "user_data,expected_status",
        [
            # Valid data
            (
                {
                    "email": "valid@example.com",
                    "password": "ValidPass123",
                    "first_name": "Valid",
                },
                status.HTTP_201_CREATED,
            ),
            # Invalid email
            (
                {
                    "email": "invalid-email",
                    "password": "ValidPass123",
                    "first_name": "Valid",
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ),
            # Password too short
            (
                {
                    "email": "valid@example.com",
                    "password": "Short1",
                    "first_name": "Valid",
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ),
            # Password without uppercase
            (
                {
                    "email": "valid@example.com",
                    "password": "password123",
                    "first_name": "Valid",
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ),
            # Password without number
            (
                {
                    "email": "valid@example.com",
                    "password": "PasswordOnly",
                    "first_name": "Valid",
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ),
            # First name too short
            (
                {
                    "email": "valid@example.com",
                    "password": "ValidPass123",
                    "first_name": "V",
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ),
        ],
    )
    def test_register_validation(
        self, test_client, user_data, expected_status, monkeypatch
    ):
        """Test register endpoint with different input validation scenarios."""
        # Only mock UserService for valid data to avoid unecessary mocking
        if expected_status == status.HTTP_201_CREATED:
            mock_create_user = AsyncMock()
            mock_user = AsyncMock()
            mock_user.id = TEST_USER_ID
            mock_user.email = user_data["email"]
            mock_user.first_name = user_data["first_name"]
            mock_create_user.return_value = mock_user

            monkeypatch.setattr(
                "app.services.user_service.UserService.create_user", mock_create_user
            )

        # Act
        response = test_client.post("/api/auth/register", json=user_data)

        # Assert
        assert response.status_code == expected_status

        # Verify mocked function was called if expecting success
        if expected_status == status.HTTP_201_CREATED:
            mock_create_user.assert_called_once_with(
                email=user_data["email"],
                password=user_data["password"],
                first_name=user_data["first_name"],
            )

            # Verify response data
            data = response.json()
            assert data["email"] == user_data["email"]
            assert data["first_name"] == user_data["first_name"]
            assert "id" in data

    @pytest.mark.parametrize(
        "credentials,auth_success,expected_status",
        [
            # Valid credentials
            (
                {"username": TEST_EMAIL, "password": TEST_PASSWORD},
                True,
                status.HTTP_200_OK,
            ),
            # Invalid credentials
            (
                {"username": TEST_EMAIL, "password": "wrong_password"},
                False,
                status.HTTP_401_UNAUTHORIZED,
            ),
            # Invalid format
            (
                {"username": "invalid-email", "password": TEST_PASSWORD},
                False,
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ),
        ],
    )
    def test_login(
        self,
        test_client,
        mock_user,
        mock_token,
        credentials,
        auth_success,
        expected_status,
        monkeypatch,
    ):
        """Test login endpoint with different scenarios."""
        if auth_success:
            # Mock successful authentication
            mock_authenticate = AsyncMock(return_value=(mock_user, mock_token))
        else:
            # Mock authentication failure with HTTPException (correct way)
            if expected_status == status.HTTP_401_UNAUTHORIZED:
                mock_authenticate = AsyncMock(
                    side_effect=HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Incorrect email or password",
                    )
                )
            else:
                # For validation errors, we don't need to mock as FastAPI handles those
                mock_authenticate = AsyncMock()

        monkeypatch.setattr(
            "app.services.auth_service.AuthService.authenticate", mock_authenticate
        )

        # Act
        response = test_client.post("/api/auth/login", json=credentials)

        # Assert
        assert response.status_code == expected_status

        # Additional assertions for successful login
        if auth_success:
            data = response.json()
            assert data["access_token"] == mock_token.access_token
            assert data["token_type"] == mock_token.token_type
            assert data["expires_in"] == mock_token.expires_in
            assert data["refresh_token"] == mock_token.refresh_token

            # Check that authenticate was called with correct credentials
            mock_authenticate.assert_called_once_with(
                credentials["username"], credentials["password"]
            )

    @pytest.mark.parametrize(
        "auth_header,refresh_success,expected_status",
        [
            # Valid token
            ("Bearer test_refresh_token", True, status.HTTP_200_OK),
            # Invalid token
            ("Bearer invalid_token", False, status.HTTP_401_UNAUTHORIZED),
            # Missing Bearer prefix
            ("test_refresh_token", False, status.HTTP_401_UNAUTHORIZED),
            # Missing token
            (None, False, status.HTTP_401_UNAUTHORIZED),
        ],
    )
    def test_refresh_token(
        self,
        test_client,
        mock_token,
        auth_header,
        refresh_success,
        expected_status,
        monkeypatch,
    ):
        """Test refresh token endpoint with different scenarios."""
        if refresh_success:
            # Mock successful token refresh
            mock_refresh = AsyncMock(return_value=mock_token)
        else:
            # Mock refresh failure with proper HTTPException
            mock_refresh = AsyncMock(
                side_effect=HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                )
            )

        monkeypatch.setattr(
            "app.services.auth_service.AuthService.refresh_token", mock_refresh
        )

        # Prepare headers
        headers = {}
        if auth_header:
            headers["Authorization"] = auth_header

        # Act
        response = test_client.post("/api/auth/refresh", headers=headers)

        # Assert
        assert response.status_code == expected_status

        # Additional assertions for successful refresh
        if refresh_success:
            data = response.json()
            assert data["access_token"] == mock_token.access_token
            assert data["token_type"] == mock_token.token_type
            assert data["expires_in"] == mock_token.expires_in
            assert data["refresh_token"] == mock_token.refresh_token

            # Check that refresh was called with correct token
            mock_refresh.assert_called_once_with("test_refresh_token")

    def test_logout(self, test_client, mock_user, monkeypatch):
        """Test logout endpoint."""
        # Mock the AuthService.logout function
        mock_logout = AsyncMock()
        monkeypatch.setattr("app.services.auth_service.AuthService.logout", mock_logout)

        # Set the dependency override for the test
        # Store original overrides to restore later
        original_overrides = app.dependency_overrides.copy()

        # This is the key part - we need to import get_current_user and override it directly
        from app.middleware.auth import get_current_user

        app.dependency_overrides[get_current_user] = lambda: mock_user

        try:
            # Act - include Authorization header
            response = test_client.post(
                "/api/auth/logout", headers={"Authorization": "Bearer dummy_token"}
            )

            # Assert
            assert response.status_code == status.HTTP_200_OK

            # Verify logout was called with correct user ID
            mock_logout.assert_called_once_with(mock_user.id)

            # Verify response message
            assert response.json() == {"message": "Successfully logged out"}
        finally:
            # Clean up - restore original dependency overrides
            app.dependency_overrides = original_overrides
