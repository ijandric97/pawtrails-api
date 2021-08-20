from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from pawtrails.core.security import Token, create_access_token
from pawtrails.core.settings import settings
from pawtrails.models.user import AddUserSchema, User, UserFullSchema

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """OAuth2 compatible token login, get an access token for future requests.
    Username field should actually contain email!
    """
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
            subject=user.uuid, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/register", response_model=UserFullSchema)
async def register(*, user_in: AddUserSchema) -> User:
    """Register a new user. Email address and username should be unique.
    You will still have to request the JWT access token via login route.
    """
    user = User.get_by_email(user_in.email) or User.get_by_username(user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this username/email already exists in the system.",
        )

    user = User(**user_in.dict())
    user.save()

    # TODO: Add email

    return user
