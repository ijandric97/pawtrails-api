from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from pawtrails.core.security import Token, create_access_token, verify_password
from pawtrails.core.settings import settings
from pawtrails.database import get_db_client
from pawtrails.models.user import AddUserSchema, User

_db_client = get_db_client()

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """OAuth2 compatible token login, get an access token for future requests.
    Username field should actually contain email!
    """
    # Get the user
    user = _db_client.get_user(email=form_data.username)

    # Check if the user actually exists and if he does if his password matches
    if not user or not verify_password(
        form_data.password, user.password  # type: ignore
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate and return the token
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            subject=user.uuid, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/register", response_model=User)
async def register(*, user_in: AddUserSchema) -> User:
    """Register a new user. Email address and username should be unique.
    You will still have to request the JWT access token via login route.
    """
    user = _db_client.get_user(email=user_in.email) or _db_client.get_user(
        username=user_in.username
    )

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this username/email already exists in the system.",
        )

    user = User(**user_in.dict())
    _db_client.create_user(user=user)

    # TODO: Add email
    return user
