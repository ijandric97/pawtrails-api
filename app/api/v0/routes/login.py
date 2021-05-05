from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_current_user
from app.core.security import create_access_token
from app.core.settings import settings
from app.models.user import User
from app.schemas.token import Token, TokenPayload
from app.schemas.user import RegisterUserSchema, UserSchema

router = APIRouter()


@router.post("/register", response_model=UserSchema)
def register(*, user_in: RegisterUserSchema) -> User:
    user = User.get_by_email(user_in.email) or User.get_by_username(user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username/email already exists in the system.",
        )

    user = User(**user_in.dict())
    user.save()

    # TODO: Add email

    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # NOTE: Username field should actually contain email!
    user = User.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/test", response_model=UserSchema)
def test(current_user: User = Depends(get_current_user)) -> Any:
    return current_user
