from typing import List, cast

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends

from pawtrails.api.deps import get_current_active_user
from pawtrails.models.location import (
    AddLocationSchema,
    Location,
    LocationSchema,
    UpdateLocationSchema,
)
from pawtrails.models.review import AddReviewSchema, Review, ReviewSchema
from pawtrails.models.user import User

router = APIRouter()


async def _check_ownership(user: User, loc: Location) -> None:
    if user not in loc.creator:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"This user {user.username} did not create this location!",
        )


@router.get("/", response_model=List[LocationSchema])
async def get_locations(skip: int = 0, limit: int = 100) -> List[Location]:
    return Location.get_all(skip, limit)


@router.post("/", response_model=LocationSchema)
async def add_location(
    loc_in: AddLocationSchema, current_user: User = Depends(get_current_active_user)
) -> Location:
    loc = Location(**loc_in.dict())
    loc.add_creator(current_user)
    loc.save()
    return loc


@router.get("/{uuid}", response_model=LocationSchema)
async def get_location(uuid: str) -> Location:
    loc = cast(Location, Location.get_by_uuid(uuid))
    if not loc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The location with the uuid {uuid} does not exist!",
        )
    return loc


@router.delete("/{uuid}", response_model=None)
async def delete_location(
    uuid: str, current_user: User = Depends(get_current_active_user)
) -> None:
    loc = await get_location(uuid)
    await _check_ownership(current_user, loc)
    loc.delete()


@router.patch("/{uuid}", response_model=LocationSchema)
async def update_location(
    loc_in: UpdateLocationSchema,
    uuid: str,
    current_user: User = Depends(get_current_active_user),
) -> Location:
    loc = await get_location(uuid)
    await _check_ownership(current_user, loc)
    loc.update(**loc_in.dict())
    loc.save()
    return loc


@router.get("/{uuid}/review", response_model=List[ReviewSchema])
async def get_reviews(uuid: str) -> None:
    loc = await get_location(uuid)
    return loc.reviews


@router.post("/{uuid}/review", response_model=ReviewSchema)
async def add_review(
    rew_in: AddReviewSchema,
    uuid: str,
    current_user: User = Depends(get_current_active_user),
) -> Review:
    loc = await get_location(uuid)
    rew = Review(**rew_in.dict())
    rew.add_writer(current_user)
    rew.add_location(loc)
    rew.save()
    return rew


@router.delete("/{uuid}/review/{review_uuid}")
async def remove_review(uuid: str) -> None:
    pass


@router.patch("/{uuid}/review/{review_uuid}")
async def update_review(uuid: str) -> None:
    pass
