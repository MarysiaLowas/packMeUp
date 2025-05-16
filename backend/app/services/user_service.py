from datetime import datetime, timedelta, timezone

UTC = timezone.utc

import logging
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from passlib.context import CryptContext  # type: ignore
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models import ActiveSession, User

# Configure logger
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        return await User.select_one(select(User).filter(User.email == email))

    @staticmethod
    async def create_user(email: str, password: str, first_name: str) -> User:
        try:
            # Create new user
            hashed_password = UserService.get_password_hash(password)
            user_data = {
                "email": email,
                "hashed_password": hashed_password,
                "first_name": first_name,
            }
            user = await User.create(**user_data)
            return user
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create user",
            )

    @staticmethod
    async def authenticate_user(email: str, password: str) -> User:
        try:
            logger.debug("Looking up user by email: %s", email)
            user = await UserService.get_user_by_email(email)

            if not user:
                logger.warning("User not found for email: %s", email)
                # Use the same error message for both cases to prevent email enumeration
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            logger.debug("Verifying password for user: %s", email)
            if not UserService.verify_password(password, user.hashed_password):
                logger.warning("Invalid password for user: %s", email)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            logger.info("User authenticated successfully: %s", email)
            return user

        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "Unexpected error during authentication: %s", str(e), exc_info=True
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication error",
            )

    @staticmethod
    async def create_session(
        user_id: UUID, refresh_token: str, expires_in_days: int = 7
    ) -> ActiveSession:
        try:
            # Remove any existing session
            await ActiveSession.delete(user_id=user_id)

            # Create new session
            expires_at = datetime.now(UTC) + timedelta(days=expires_in_days)
            session_data = {
                "user_id": user_id,
                "refresh_token": refresh_token,
                "expires_at": expires_at,
            }
            session = await ActiveSession.create(**session_data)
            return session
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create session",
            )

    @staticmethod
    async def get_active_session(user_id: UUID) -> Optional[ActiveSession]:
        try:
            return await ActiveSession.select_one(
                select(ActiveSession)
                .filter(ActiveSession.user_id == user_id)
                .filter(ActiveSession.expires_at > datetime.now(UTC))
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not get session",
            )

    @staticmethod
    async def delete_session(user_id: UUID) -> None:
        try:
            await ActiveSession.delete(user_id=user_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not delete session",
            )
