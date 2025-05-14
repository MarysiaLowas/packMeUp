from datetime import datetime, timedelta, timezone
UTC = timezone.utc

from typing import Optional, Dict
from uuid import UUID
import os
import logging

from fastapi import HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel

from app.services.user_service import UserService
from app.models import User

# Configure logger
logger = logging.getLogger(__name__)

# JWT Configuration
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
logger.info("JWT_SECRET_KEY is set: %s", bool(JWT_SECRET_KEY))

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int  # seconds
    refresh_token: str

class TokenData(BaseModel):
    user_id: UUID
    email: str

class AuthService:
    @staticmethod
    def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(user_id: UUID) -> str:
        expire = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode = {
            "sub": str(user_id),
            "exp": expire
        }
        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> TokenData:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            user_id = UUID(payload.get("sub"))
            email = payload.get("email")
            if user_id is None or email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                )
            return TokenData(user_id=user_id, email=email)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    @staticmethod
    async def authenticate(email: str, password: str) -> tuple[User, Token]:
        try:
            logger.info("Starting authentication process for email: %s", email)
            logger.info("JWT_SECRET_KEY is set: %s", bool(os.environ.get("JWT_SECRET_KEY")))
            
            logger.debug("Attempting to authenticate user with UserService")
            user = await UserService.authenticate_user(email, password)
            logger.info("User authenticated successfully: %s", user.email)
            
            # Create access token
            logger.debug("Creating access token")
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = AuthService.create_access_token(
                data={"sub": str(user.id), "email": user.email, "first_name": user.first_name},
                expires_delta=access_token_expires
            )
            logger.debug("Access token created successfully")
            
            # Create refresh token and session
            logger.debug("Creating refresh token")
            refresh_token = AuthService.create_refresh_token(user.id)
            logger.debug("Creating user session")
            await UserService.create_session(user.id, refresh_token)
            logger.info("Session created successfully for user: %s", user.email)
            
            token = Token(
                access_token=access_token,
                token_type="bearer",
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                refresh_token=refresh_token
            )
            
            logger.info("Authentication completed successfully for user: %s", user.email)
            return user, token
            
        except Exception as e:
            logger.error("Authentication failed with error: %s", str(e), exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication failed",
            )

    @staticmethod
    async def refresh_token(refresh_token: str) -> Token:
        try:
            logger.info("Attempting to refresh token")
            payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            user_id = UUID(payload.get("sub"))
            logger.debug("Decoded refresh token for user_id: %s", user_id)
            
            # Verify session exists and is valid
            session = await UserService.get_active_session(user_id)
            if not session:
                logger.warning("No active session found for user_id: %s", user_id)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token - no active session",
                )
            
            if session.refresh_token != refresh_token:
                logger.warning("Refresh token mismatch for user_id: %s", user_id)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token - token mismatch",
                )
            
            # Get user
            user = await User.get(id=user_id)
            logger.info("Found user for refresh: %s", user.email)
            
            # Create new access token
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = AuthService.create_access_token(
                data={"sub": str(user.id), "email": user.email, "first_name": user.first_name},
                expires_delta=access_token_expires
            )
            logger.info("Successfully refreshed token for user: %s", user.email)
            
            return Token(
                access_token=access_token,
                token_type="bearer",
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                refresh_token=refresh_token
            )
            
        except JWTError as e:
            logger.error("JWT decode error during refresh: %s", str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token - JWT error",
            )
        except Exception as e:
            logger.error("Unexpected error during token refresh: %s", str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token - unexpected error",
            )

    @staticmethod
    async def logout(user_id: UUID) -> None:
        await UserService.delete_session(user_id) 