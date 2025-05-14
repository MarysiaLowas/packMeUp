from typing import Annotated, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.models import User
from app.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        token_data = AuthService.verify_token(token)
        user = await User.get(id=token_data.user_id)
        return user
    except (JWTError, HTTPException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_optional_user(token: Annotated[Optional[str], Depends(oauth2_scheme)]) -> Optional[User]:
    if not token:
        return None
    try:
        token_data = AuthService.verify_token(token)
        user = await User.get(id=token_data.user_id)
        return user
    except (JWTError, HTTPException):
        return None 