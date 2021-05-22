from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from pawtrails.api.deps import get_current_active_user, get_current_user
from pawtrails.models.pet import Pet, PetSchema
from pawtrails.models.user import UpdateUserSchema, User, UserFullSchema, UserSchema

router = APIRouter()


@router.get("/", response_model=UserFullSchema)
async def get_my_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.delete("/")
async def delete_user(current_user: User = Depends(get_current_user)) -> None:
    current_user.delete()


@router.patch("/", response_model=UserFullSchema)
async def update_user(
    user_in: UpdateUserSchema, current_user: User = Depends(get_current_user)
) -> User:
    if user_in.email:
        try:
            current_user.email = user_in.email
            print("OH NO", flush=True)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The user with this email already exists in our system.",
            )
    if user_in.username:
        try:
            current_user.username = user_in.username
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The user with this username already exists in our system.",
            )
    if user_in.password:
        current_user.password = user_in.password

    current_user.save()
    return current_user


@router.post("/follow", response_model=UserSchema)
async def follow_user(
    uuid: str, current_user: User = Depends(get_current_active_user)
) -> User:
    user = await get_user_by_uuid(uuid)
    if not current_user.add_following(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You tried to follow already followed user or yourself.",
        )

    return user


@router.delete("/follow")
async def unfollow_user(
    uuid: str, current_user: User = Depends(get_current_active_user)
) -> None:
    user = await get_user_by_uuid(uuid)
    if not current_user.remove_following(user):
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


@router.get("/following", response_model=List[UserSchema])
async def get_following(
    current_user: User = Depends(get_current_active_user),
) -> List[User]:
    return current_user.following


@router.get("/pets", response_model=List[PetSchema])
async def get_pets(current_user: User = Depends(get_current_user)) -> List[Pet]:
    return current_user.pets


@router.get("/list", response_model=List[UserSchema])
async def get_user_list(skip: int = 0, limit: int = 100) -> List[User]:
    return User.get_all(skip, limit)


@router.get("/{uuid}", response_model=UserSchema)
async def get_user_by_uuid(uuid: str) -> User:
    user = User.get_by_uuid(uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with uuid {uuid} does not exist",
        )

    return user


@router.get("/{uuid}/followers", response_model=List[UserSchema])
async def get_followers_by_uuid(uuid: str) -> List[User]:
    user = await get_user_by_uuid(uuid)
    return user.followers


@router.get("/{uuid}/following", response_model=List[UserSchema])
async def get_following_by_uuid(uuid: str) -> List[User]:
    user = await get_user_by_uuid(uuid)
    return user.following


@router.get("/{uuid}/pets", response_model=List[PetSchema])
async def get_pets_by_uuid(uuid: str) -> List[Pet]:
    user = await get_user_by_uuid(uuid)  # NOTE: coroutines have to be awaited
    return user.pets
