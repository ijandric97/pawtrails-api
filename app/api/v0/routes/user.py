from typing import List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from app.api.deps import get_current_active_user, get_current_user
from app.models.user import User, UserSchema

router = APIRouter()


@router.post("/me", response_model=UserSchema)
async def get_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.get("/list", response_model=List[str])
async def get_user_list(skip: int = 0, limit: int = 100) -> Optional[List[str]]:
    ret: List[str] = []

    for user in User.get_all(skip, limit):
        print(user.username, flush=True)
        ret.append(user.username)

    return ret


@router.get(
    "/username/{username}",
    response_model=UserSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def get_user_by_username(username: str) -> User:
    return User.get_by_username(username)


@router.get(
    "/email/{email}",
    response_model=UserSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def get_user_by_email(email: str) -> User:
    return User.get_by_email(email)


@router.post("/follow/{email}", response_model=UserSchema)
async def follow_user(
    email: str, current_user: User = Depends(get_current_active_user)
) -> User:
    user = User.get_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} does not exist",
        )
    if not current_user.follow(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You tried to follow yourself or are already following this user",
        )

    return user


@router.post("/unfollow/{email}", response_model=UserSchema)
async def unfollow_user(
    email: str, current_user: User = Depends(get_current_active_user)
) -> User:
    user = User.get_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} does not exist",
        )
    if not current_user.unfollow(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You tried to unfollow yourself or someone you are not following",
        )

    return user


@router.get("/followers", response_model=List[UserSchema])
async def get_followers(
    current_user: User = Depends(get_current_active_user),
) -> List[User]:
    return current_user.followers


@router.get("/following", response_model=List[UserSchema])
async def get_following(
    current_user: User = Depends(get_current_active_user),
) -> List[User]:
    return current_user.following
