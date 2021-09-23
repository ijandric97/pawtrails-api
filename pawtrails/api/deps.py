from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from pawtrails.core.security import TokenData
from pawtrails.core.settings import settings
from pawtrails.database import get_db_client
from pawtrails.models.user import User

_db_client = get_db_client()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/login")
"""The bearer token that is fetched from the header"""


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Returns the currently logged in user.

    Extracts the UUID of the user from the provided JWT token and returns the
    corresponding User object.

    Args:
        token (str, optional): A JWT string (token). Fetched from the bearer token
            header. Defaults to Depends(oauth2_scheme).

    Raises:
        HTTPException: (401 UNAUTHORIZED) Invalid JWT token
        HTTPException: (404 NOT FOUND) User is not found (somehow)

    Returns:
        User: Currently logged in user if everythig was ok.
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenData(uuid=payload.get("sub"))
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = _db_client.get_user(uuid=token_data.uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Returns the currently logged in user, but only if he is active

    Extracts the UUID of the user from the provided JWT token and returns the
    corresponding User object only if it has is_active set to true.

    Args:
        current_user (User, optional): The currently logged in user. Fetched from the
            get_current_user function which fetches it from the bearer token.
            Defaults to Depends(get_current_user).

    Raises:
        HTTPException: (400 BAD REQUEST) The user is indeed inactive
        * Can also raise everything specified in get_current_user

    Returns:
        User: Currently logged in active user if everythig was ok.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user
