from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel as Schema

from pawtrails.core.settings import settings


class Token(Schema):
    """
    A structure containing the JWT access token and its type (e.g. bearer)
    """

    access_token: str
    """The JWT access token"""

    token_type: str
    """Type of the JWT token (for example: 'bearer')"""


class TokenData(Schema):
    """
    A structure which contains the data that should be encoded in the Token.
    For now that is only the UUID of the currently logged in user.
    """

    uuid: str = ""
    """Unique record ID of the currently logged in user."""


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""A reference to the bcrypt CryptContext object."""


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Creates a JWT access token for the logged in user

    Args:
        subject (Union[str, Any]): Data which you wish to encode
        expires_delta (Optional[timedelta]): How long it will last. Defaults to None.

    Returns:
        str: A JWT encoded access token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if the RAW password matches the provided HMAC-SHA256 hash.

    Args:
        plain_password (str): RAW password
        hashed_password (str): HMAC-SHA256 hash

    Returns:
        bool: True if the password matches the hash
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generates a HMAC-SHA256 hash for the given RAW password

    Args:
        password (str): The original RAW password

    Returns:
        str: HMAC-SHA256 hash of the given RAW password
    """
    return pwd_context.hash(password)
