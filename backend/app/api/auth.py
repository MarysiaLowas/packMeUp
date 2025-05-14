from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field

from app.models import User
from app.services.auth_service import AuthService, Token
from app.services.user_service import UserService
from app.middleware.auth import get_current_user

router = APIRouter(tags=["auth"])

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

@router.post("/login", response_model=Token)
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user, token = await AuthService.authenticate(form_data.username, form_data.password)
    
    # Set refresh token in httpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=token.refresh_token,
        httponly=True,
        secure=True,  # Only send cookie over HTTPS
        samesite="lax",  # Protect against CSRF
        max_age=7 * 24 * 60 * 60  # 7 days in seconds
    )
    
    return token

@router.post("/refresh", response_model=Token)
async def refresh_token(
    response: Response,
    refresh_token: str = Depends(lambda x: x.cookies.get("refresh_token"))
) -> Token:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing"
        )
    
    token = await AuthService.refresh_token(refresh_token)
    return token

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
        secure=True,
        samesite="lax"
    )
    
    return {"message": "Successfully logged out"} 