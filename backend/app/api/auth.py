from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status, Request, Header
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field

from app.models import User
from app.services.auth_service import AuthService, Token
from app.services.user_service import UserService
from app.middleware.auth import get_current_user
from app.config import DEV_MODE
import logging

router = APIRouter(tags=["auth"])

logger = logging.getLogger(__name__)

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        pattern=r".*[A-Z].*[0-9].*|.*[0-9].*[A-Z].*",
        description="Password must be at least 8 characters long and contain at least one uppercase letter and one number"
    )
    first_name: str = Field(min_length=2, max_length=50)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "StrongPass123",
                "first_name": "Jan"
            }
        }
    }

class UserResponse(BaseModel):
    id: UUID
    email: str
    first_name: str

    class Config:
        from_attributes = True

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate) -> User:
    return await UserService.create_user(
        email=user_data.email,
        password=user_data.password,
        first_name=user_data.first_name
    )

def set_auth_cookie(response: Response, token: str):
    """Helper function to set auth cookie with proper settings based on environment"""
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        secure=not DEV_MODE,  # Only require HTTPS in production
        samesite="lax" if DEV_MODE else "strict",  # More relaxed in development
        max_age=7 * 24 * 60 * 60  # 7 days in seconds
    )

@router.post("/login", response_model=Token)
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    logger.info("Login attempt for user: %s", form_data.username)
    user, token = await AuthService.authenticate(form_data.username, form_data.password)
    logger.info("Login successful for user: %s", form_data.username)
    return token

@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: Request,
    response: Response,
    auth: str = Header(None, alias="Authorization")
) -> Token:
    logger.info("Refresh token request received")
    logger.debug("Request headers: %s", request.headers)
    
    if not auth or not auth.startswith("Bearer "):
        logger.warning("No Bearer token in Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing"
        )
    
    refresh_token = auth.split(" ")[1]
    logger.debug("Refresh token found in Authorization header")
    
    try:
        token = await AuthService.refresh_token(refresh_token)
        logger.info("Token refreshed successfully")
        return token
    except Exception as e:
        logger.error("Failed to refresh token: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.post("/logout")
async def logout(
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)]
):
    await AuthService.logout(current_user.id)
    
    # Clear refresh token cookie
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=not DEV_MODE,
        samesite="lax" if DEV_MODE else "strict"
    )
    
    return {"message": "Successfully logged out"} 