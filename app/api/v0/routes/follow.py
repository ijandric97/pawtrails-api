from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from app.api.deps import get_current_active_user
from app.models.user import User, UserSchema

router = APIRouter()


@router.post("/{uuid}", response_model=UserSchema)
async def follow_user(
    uuid: str, current_user: User = Depends(get_current_active_user)
) -> User:
    user = User.get_by_uuid(uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with uuid {uuid} does not exist.",
        )
    if not current_user.follow(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You tried to follow already followed user or yourself.",
        )

    return user


@router.delete("/{uuid}")
async def unfollow_user(
    uuid: str, current_user: User = Depends(get_current_active_user)
) -> None:
    user = User.get_by_uuid(uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with uuid {uuid} does not exist.",
        )
    if not current_user.unfollow(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You tried to unfollow yourself or someone you are not following.",
        )

    return None


@router.get("/followers", response_model=List[UserSchema])
async def get_followers(
    current_user: User = Depends(get_current_active_user),
) -> List[User]:
    return current_user.followers


@router.get(
    "/followers/{uuid}",
    response_model=List[UserSchema],
    dependencies=[Depends(get_current_active_user)],
)
async def get_followers_by_uuid(
    uuid: str,
) -> List[User]:
    user = User.get_by_uuid(uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with uuid {uuid} does not exist",
        )

    return user.followers


@router.get("/following", response_model=List[UserSchema])
async def get_following(
    current_user: User = Depends(get_current_active_user),
) -> List[User]:
    return current_user.following


@router.get(
    "/following/{uuid}",
    response_model=List[UserSchema],
    dependencies=[Depends(get_current_active_user)],
)
async def get_following_by_uuid(uuid: str) -> List[User]:
    user = User.get_by_uuid(uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with uuid {uuid} does not exist",
        )

    return user.following
