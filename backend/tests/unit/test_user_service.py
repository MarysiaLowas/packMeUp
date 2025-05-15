import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import uuid
import bcrypt
from fastapi import HTTPException
from sqlalchemy import select

from app.services.user_service import UserService
from app.models import User, ActiveSession

# Test constants
TEST_USER_ID = uuid.uuid4()
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "StrongPass123"
TEST_FIRST_NAME = "Test"
TEST_HASHED_PASSWORD = bcrypt.hashpw("StrongPass123".encode(), bcrypt.gensalt()).decode()
TEST_REFRESH_TOKEN = "test_refresh_token"

@pytest.fixture
def mock_user():
    """Create a mock user for testing"""
    user = AsyncMock(spec=User)
    user.id = TEST_USER_ID
    user.email = TEST_EMAIL
    user.first_name = TEST_FIRST_NAME
    user.hashed_password = TEST_HASHED_PASSWORD
    return user

@pytest.fixture
def mock_session():
    """Create a mock user session for testing"""
    session = AsyncMock(spec=ActiveSession)
    session.user_id = TEST_USER_ID
    session.refresh_token = TEST_REFRESH_TOKEN
    session.is_active = True
    return session

class TestUserService:
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "user_exists", [
            True,
            False
        ]
    )
    async def test_create_user(self, user_exists):
        """Test creating a new user"""
        # Arrange
        # Mock User.create - zawsze potrzebujemy mocka
        mock_user = AsyncMock(spec=User)
        mock_user.id = TEST_USER_ID
        mock_user.email = TEST_EMAIL
        mock_user.first_name = TEST_FIRST_NAME
        
        if user_exists:
            # Przypadek gdy użytkownik już istnieje - create rzuca IntegrityError
            from sqlalchemy.exc import IntegrityError
            with patch("app.models.User.create", new_callable=AsyncMock) as mock_create:
                mock_create.side_effect = IntegrityError("", "", "")
                
                # Act & Assert - oczekujemy HTTPException
                with pytest.raises(HTTPException) as exc_info:
                    await UserService.create_user(TEST_EMAIL, TEST_PASSWORD, TEST_FIRST_NAME)
                assert exc_info.value.status_code == 400
                assert "already registered" in exc_info.value.detail
        else:
            # Przypadek gdy użytkownik nie istnieje - create zwraca użytkownika
            with patch("app.models.User.create", new_callable=AsyncMock) as mock_create:
                mock_create.return_value = mock_user
                
                # Act
                result = await UserService.create_user(TEST_EMAIL, TEST_PASSWORD, TEST_FIRST_NAME)
                
                # Assert
                assert result == mock_user
                
                # Check that create was called with correct parameters
                # Including a hashed password
                mock_create.assert_called_once()
                create_args = mock_create.call_args[1]
                assert create_args["email"] == TEST_EMAIL
                assert create_args["first_name"] == TEST_FIRST_NAME
                assert bcrypt.checkpw(
                    TEST_PASSWORD.encode(),
                    create_args["hashed_password"].encode()
                )
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "password_valid", [
            True,
            False
        ]
    )
    async def test_authenticate_user(self, mock_user, password_valid):
        """Test authenticating a user with valid and invalid credentials"""
        # Arrange
        with patch("app.services.user_service.UserService.get_user_by_email", new_callable=AsyncMock) as mock_get_user:
            if password_valid:
                # For valid password test, return the mock user
                mock_get_user.return_value = mock_user
                
                # Mock bcrypt.checkpw to return True (password match)
                with patch("app.services.user_service.UserService.verify_password", return_value=True):
                    # Act
                    result = await UserService.authenticate_user(TEST_EMAIL, TEST_PASSWORD)
                    
                    # Assert
                    assert result == mock_user
                    mock_get_user.assert_called_once_with(TEST_EMAIL)
            else:
                # For invalid password test
                with patch("app.services.user_service.UserService.verify_password", return_value=False):
                    # Either user not found or password incorrect
                    if password_valid is False:
                        mock_get_user.return_value = mock_user
                    else:
                        mock_get_user.return_value = None
                    
                    # Act & Assert
                    with pytest.raises(HTTPException) as exc_info:
                        await UserService.authenticate_user(TEST_EMAIL, TEST_PASSWORD)
                    assert exc_info.value.status_code == 401
                    assert "Incorrect email or password" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_create_session(self):
        """Test creating a user session"""
        # Arrange
        with patch("app.models.ActiveSession.delete", new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = None
            
            # Mock ActiveSession.create for the new session
            with patch("app.models.ActiveSession.create", new_callable=AsyncMock) as mock_create:
                mock_create.return_value = AsyncMock(spec=ActiveSession)
                
                # Act
                await UserService.create_session(TEST_USER_ID, TEST_REFRESH_TOKEN)
                
                # Assert
                # Check that existing sessions were deleted
                mock_delete.assert_called_once_with(user_id=TEST_USER_ID)
                
                # Check that a new session was created with correct args
                mock_create.assert_called_once()
                create_args = mock_create.call_args[1]
                assert create_args["user_id"] == TEST_USER_ID
                assert create_args["refresh_token"] == TEST_REFRESH_TOKEN
                assert "expires_at" in create_args
    
    @pytest.mark.asyncio
    async def test_get_active_session(self, mock_session):
        """Test retrieving an active user session"""
        # Arrange
        with patch("app.models.ActiveSession.select_one", new_callable=AsyncMock) as mock_select_one:
            mock_select_one.return_value = mock_session
            
            # Act
            result = await UserService.get_active_session(TEST_USER_ID)
            
            # Assert
            assert result == mock_session
            mock_select_one.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_session(self):
        """Test deleting user sessions"""
        # Arrange
        with patch("app.models.ActiveSession.delete", new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = None
            
            # Act
            await UserService.delete_session(TEST_USER_ID)
            
            # Assert
            mock_delete.assert_called_once_with(user_id=TEST_USER_ID) 