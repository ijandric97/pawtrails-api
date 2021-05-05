from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_current_active_user
from app.core.security import Token, create_access_token
from app.core.settings import settings
from app.models.user import RegisterUserSchema, User, UserSchema

router = APIRouter()


@router.post("/register", response_model=UserSchema)
async def register(*, user_in: RegisterUserSchema) -> User:
    user = User.get_by_email(user_in.email) or User.get_by_username(user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username/email already exists in the system.",
        )

    user = User(**user_in.dict())
    user.save()

    # TODO: Add email

    return user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # NOTE: Username field should actually contain email!
    user = User.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": create_access_token(
            subject=user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/test", response_model=UserSchema)
async def test(current_user: User = Depends(get_current_active_user)) -> Any:
    return current_user
