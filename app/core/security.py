from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.settings import settings

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """Creates a JWT acces token for the logged in user

    Args:
        subject (Union[str, Any]): [description]
        expires_delta (timedelta, optional): [description]. Defaults to None.

    Returns:
        str: A JWT encoded access token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
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
