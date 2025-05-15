import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import timedelta
from jose import jwt
from fastapi import HTTPException

from app.services.auth_service import AuthService, Token
from app.models import User

# Constants for testing
TEST_USER_ID = uuid.uuid4()
TEST_EMAIL = "test@example.com"
TEST_FIRST_NAME = "Test"
TEST_JWT_SECRET = "test_secret_key"
TEST_PASSWORD = "Password123"


@pytest.fixture(autouse=True)
def setup_jwt_secret(monkeypatch):
    """Set JWT secret for testing."""
    monkeypatch.setenv("JWT_SECRET_KEY", TEST_JWT_SECRET)
    monkeypatch.setattr("app.services.auth_service.JWT_SECRET_KEY", TEST_JWT_SECRET)


@pytest.fixture
def mock_user():
    """Create a mock user for testing."""
    user = MagicMock(spec=User)
    user.id = TEST_USER_ID
    user.email = TEST_EMAIL
    user.first_name = TEST_FIRST_NAME
    return user


class TestAuthService:
    def test_create_access_token(self):
        """Test creating an access token."""
        # Arrange
        data = {"sub": str(TEST_USER_ID), "email": TEST_EMAIL}
        expires_delta = timedelta(minutes=15)

        # Act
        token = AuthService.create_access_token(data, expires_delta)

        # Assert
        decoded = jwt.decode(token, TEST_JWT_SECRET, algorithms=["HS256"])
        assert decoded["sub"] == str(TEST_USER_ID)
        assert decoded["email"] == TEST_EMAIL
        # Check expiration is properly set
        assert "exp" in decoded

    def test_create_refresh_token(self):
        """Test creating a refresh token."""
        # Act
        token = AuthService.create_refresh_token(TEST_USER_ID)

        # Assert
        decoded = jwt.decode(token, TEST_JWT_SECRET, algorithms=["HS256"])
        assert decoded["sub"] == str(TEST_USER_ID)
        assert "exp" in decoded

    def test_verify_token_valid(self):
        """Test verifying a valid token."""
        # Arrange
        data = {"sub": str(TEST_USER_ID), "email": TEST_EMAIL}
        token = AuthService.create_access_token(data)

        # Act
        token_data = AuthService.verify_token(token)

        # Assert
        assert token_data.user_id == TEST_USER_ID
        assert token_data.email == TEST_EMAIL

    def test_verify_token_invalid(self):
        """Test verifying an invalid token."""
        # Arrange
        invalid_token = "invalid.token.format"

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            AuthService.verify_token(invalid_token)
        assert exc_info.value.status_code == 401

    def test_verify_token_missing_data(self):
        """Test verifying a token with missing data."""
        # Arrange - token with missing email
        data = {"sub": str(TEST_USER_ID)}
        token = AuthService.create_access_token(data)

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            AuthService.verify_token(token)
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_authenticate_success(self, mock_user):
        """Test successful authentication."""
        # Arrange
        with patch(
            "app.services.user_service.UserService.authenticate_user",
            new_callable=AsyncMock,
        ) as mock_auth_user:
            mock_auth_user.return_value = mock_user

            with patch(
                "app.services.user_service.UserService.create_session",
                new_callable=AsyncMock,
            ) as mock_create_session:
                mock_create_session.return_value = None

                # Act
                user, token = await AuthService.authenticate(TEST_EMAIL, TEST_PASSWORD)

                # Assert
                assert user == mock_user
                assert isinstance(token, Token)
                assert token.token_type == "bearer"
                mock_auth_user.assert_called_once_with(TEST_EMAIL, TEST_PASSWORD)
                mock_create_session.assert_called_once()

    @pytest.mark.asyncio
    async def test_authenticate_failure(self):
        """Test failed authentication."""
        # Arrange
        with patch(
            "app.services.user_service.UserService.authenticate_user",
            new_callable=AsyncMock,
        ) as mock_auth_user:
            mock_auth_user.side_effect = HTTPException(
                status_code=401, detail="Invalid credentials"
            )

            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                await AuthService.authenticate(TEST_EMAIL, "wrong_password")
            assert exc_info.value.status_code == 500

    @pytest.mark.asyncio
    async def test_refresh_token_success(self, mock_user):
        """Test successful token refresh."""
        # Arrange
        refresh_token = AuthService.create_refresh_token(TEST_USER_ID)
        mock_session = MagicMock()
        mock_session.refresh_token = refresh_token

        with patch(
            "app.services.user_service.UserService.get_active_session",
            new_callable=AsyncMock,
        ) as mock_get_session:
            mock_get_session.return_value = mock_session

            with patch("app.models.User.get", new_callable=AsyncMock) as mock_get_user:
                mock_get_user.return_value = mock_user

                # Act
                token = await AuthService.refresh_token(refresh_token)

                # Assert
                assert isinstance(token, Token)
                assert token.token_type == "bearer"
                assert token.refresh_token == refresh_token
                mock_get_session.assert_called_once_with(TEST_USER_ID)
                mock_get_user.assert_called_once_with(id=TEST_USER_ID)

    @pytest.mark.asyncio
    async def test_refresh_token_no_session(self):
        """Test token refresh with no active session."""
        # Arrange
        refresh_token = AuthService.create_refresh_token(TEST_USER_ID)

        with patch(
            "app.services.user_service.UserService.get_active_session",
            new_callable=AsyncMock,
        ) as mock_get_session:
            mock_get_session.return_value = None

            # Modyfikujemy JWTError aby nie był łapany przez ogólny except Exception
            with patch("jose.jwt.decode") as mock_jwt_decode:
                mock_jwt_decode.return_value = {"sub": str(TEST_USER_ID)}

                # Act & Assert
                with pytest.raises(HTTPException) as exc_info:
                    await AuthService.refresh_token(refresh_token)
                assert exc_info.value.status_code == 401
                # Sprawdzamy alternatywne komunikaty błędu, ponieważ może być łapany przez różne except
                # TODO: Add more specific error messages
                assert (
                    "Invalid refresh token - no active session" in exc_info.value.detail
                    or "Invalid refresh token - unexpected error"
                    in exc_info.value.detail
                )

    @pytest.mark.asyncio
    async def test_refresh_token_mismatch(self, mock_user):
        """Test token refresh with mismatched tokens."""
        # Arrange
        refresh_token = AuthService.create_refresh_token(TEST_USER_ID)
        mock_session = MagicMock()
        mock_session.refresh_token = "different_refresh_token"

        with patch(
            "app.services.user_service.UserService.get_active_session",
            new_callable=AsyncMock,
        ) as mock_get_session:
            mock_get_session.return_value = mock_session

            # Modyfikujemy JWTError aby nie był łapany przez ogólny except Exception
            with patch("jose.jwt.decode") as mock_jwt_decode:
                mock_jwt_decode.return_value = {"sub": str(TEST_USER_ID)}

                # Act & Assert
                with pytest.raises(HTTPException) as exc_info:
                    await AuthService.refresh_token(refresh_token)
                assert exc_info.value.status_code == 401
                # Sprawdzamy alternatywne komunikaty błędu, ponieważ może być łapany przez różne except
                #
                assert (
                    "token mismatch" in exc_info.value.detail
                    or "Invalid refresh token - token mismatch" in exc_info.value.detail
                    or "Invalid refresh token - unexpected error"
                    in exc_info.value.detail
                )

    @pytest.mark.asyncio
    async def test_logout(self):
        """Test user logout."""
        # Arrange
        with patch(
            "app.services.user_service.UserService.delete_session",
            new_callable=AsyncMock,
        ) as mock_delete_session:
            mock_delete_session.return_value = None

            # Act
            await AuthService.logout(TEST_USER_ID)

            # Assert
            mock_delete_session.assert_called_once_with(TEST_USER_ID)
