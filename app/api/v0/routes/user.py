from typing import List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from pydantic.networks import EmailStr

from app.api.deps import get_current_active_user, get_current_user
from app.models.pet import Pet, PetSchema
from app.models.user import User, UserFullSchema, UserSchema

router = APIRouter()


@router.get("/", response_model=UserFullSchema)
async def get_my_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.delete("/")
async def delete_user(current_user: User = Depends(get_current_user)) -> None:
    current_user.delete()


@router.get("/list", response_model=List[UserSchema])
async def get_user_list(skip: int = 0, limit: int = 100) -> Optional[List[User]]:
    return User.get_all(skip, limit)


@router.get("/uuid/{uuid}", response_model=UserSchema)
async def get_user_by_uuid(uuid: str) -> User:
    user = User.get_by_uuid(uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with uuid {uuid} does not exist",
        )

    return user


@router.get("/username/{username}", response_model=UserSchema)
async def get_user_by_username(username: str) -> User:
    user = User.get_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} does not exist",
        )

    return user


@router.put("/email", response_model=UserFullSchema)
async def change_email(
    email: EmailStr, current_user: User = Depends(get_current_user)
) -> User:
    try:
        current_user.email = email
        current_user.save()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already exists in our system.",
        )
    return current_user


@router.put("/username", response_model=UserFullSchema)
async def change_username(
    username: str, current_user: User = Depends(get_current_user)
) -> User:
    try:
        current_user.username = username
        current_user.save()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this username already exists in our system.",
        )
    return current_user


@router.put("/password", response_model=UserFullSchema)
async def change_password(
    password: str, current_user: User = Depends(get_current_user)
) -> User:
    """Change your current password with something new."""
    current_user.password = password
    current_user.save()
    return current_user


@router.post("/follow/{uuid}", response_model=UserSchema)
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


@router.delete("/follow/{uuid}")
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


@router.get("/followers/{uuid}", response_model=List[UserSchema])
async def get_followers_by_uuid(uuid: str) -> List[User]:
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


@router.get("/following/{uuid}", response_model=List[UserSchema])
async def get_following_by_uuid(uuid: str) -> List[User]:
    user = User.get_by_uuid(uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with uuid {uuid} does not exist",
        )

    return user.following


@router.get("/pets", response_model=List[PetSchema])
async def get_pets(current_user: User = Depends(get_current_user)) -> List[Pet]:
    return current_user.pets


@router.get("/pets/{uuid}", response_model=List[PetSchema])
async def get_pets_by_uuid(uuid: str) -> List[Pet]:
    user = User.get_by_uuid(uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with uuid {uuid} does not exist",
        )

    return user.pets
