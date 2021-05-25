from typing import List

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from pawtrails.models.location import Location, LocationSchema
from pawtrails.models.pet import Pet, PetSchema
from pawtrails.models.review import Review, ReviewSchema
from pawtrails.models.user import User, UserSchema

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
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


@router.get("/{uuid}/locations", response_model=List[LocationSchema])
async def get_locations_by_uuid(uuid: str) -> List[Location]:
    user = await get_user_by_uuid(uuid)
    return user.locations


@router.get("/{uuid}/favorites", response_model=List[LocationSchema])
async def get_favorites_by_uuid(uuid: str) -> List[Location]:
    user = await get_user_by_uuid(uuid)
    return user.favorites


@router.get("/{uuid}/reviews", response_model=List[ReviewSchema])
async def get_reviews_by_uuid(uuid: str) -> List[Review]:
    user = await get_user_by_uuid(uuid)
    return user.reviews
