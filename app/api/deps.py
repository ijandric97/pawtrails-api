from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app.core import security
from app.core.settings import settings
from app.models.user import User
from app.schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/login")


def get_current_user(token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        print("MOOD", flush=True)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = User.get_by_email(email=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
