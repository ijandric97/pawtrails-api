from typing import List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from app.api.deps import get_current_active_user, get_current_user
from app.models.user import User, UserFullSchema, UserSchema

router = APIRouter()


@router.get("/", response_model=UserFullSchema)
async def get_my_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.delete("/")
async def delete_user(current_user: User = Depends(get_current_user)) -> None:
    current_user.delete()


@router.get("/list", response_model=List[str])
async def get_user_list(skip: int = 0, limit: int = 100) -> Optional[List[str]]:
    ret: List[str] = []

    for user in User.get_all(skip, limit):
        print(user.username, flush=True)
        ret.append(user.username)

    return ret


@router.get(
    "/uuid/{uuid}",
    response_model=UserSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def get_user_by_uuid(uuid: str) -> User:
    user = User.get_by_uuid(uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with uuid {uuid} does not exist",
        )

    return user


@router.get(
    "/username/{username}",
    response_model=UserSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def get_user_by_username(username: str) -> User:
    user = User.get_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} does not exist",
        )

    return user
