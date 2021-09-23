from typing import List, cast

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends

from pawtrails.api.deps import get_current_active_user
from pawtrails.models.location import (
    AddLocationSchema,
    Location,
    SearchLocationDistanceOptions,
    SearchLocationOptions,
    SearchLocationSchema,
    SearchLocationUserOptions,
    UpdateLocationSchema,
)
from pawtrails.models.review import AddReviewSchema, Review, UpdateReviewSchema
from pawtrails.models.user import User

router = APIRouter()


async def _check_ownership(user: User, loc: Location) -> None:
    if user != loc.creator:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"This user {user.username} did not create this location!",
        )


@router.get("/", response_model=List[Location])
async def get_locations(skip: int = 0, limit: int = 100) -> List[Location]:
    return Location.get_all(skip, limit)


@router.post("/search", response_model=List[Location])
async def search_locations(
    search_in: SearchLocationSchema,
    current_user: User = Depends(get_current_active_user),
) -> List[Location]:
    params = SearchLocationOptions(**search_in.dict())
    if search_in.created or search_in.favorited:
        params.user = SearchLocationUserOptions(
            uuid=current_user.uuid,
            created=search_in.created,
            favorited=search_in.favorited,
        )
    if search_in.longitude and search_in.latitude and search_in.max_distance:
        params.distance = SearchLocationDistanceOptions(
            longitude=search_in.longitude,
            latitude=search_in.latitude,
            max=search_in.max_distance,
        )

    return Location.search(params)


@router.post("/", response_model=Location)
async def add_location(
    loc_in: AddLocationSchema, current_user: User = Depends(get_current_active_user)
) -> Location:
    loc = Location(**loc_in.dict())
    loc.add_creator(current_user)
    loc.save()
    return loc


@router.get("/{uuid}", response_model=Location)
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


@router.patch("/{uuid}", response_model=Location)
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


@router.get("/{uuid}/favorite", response_model=List[User])
async def get_location_favorites(uuid: str) -> List[User]:
    loc = await get_location(uuid)
    return loc.favorites


@router.post("/{uuid}/favorite", response_model=User)
async def add_favorite(
    uuid: str, current_user: User = Depends(get_current_active_user)
) -> User:
    loc = await get_location(uuid)
    current_user.add_favorite(loc)
    current_user.save()
    return current_user


@router.delete("/{uuid}/favorite", response_model=None)
async def remove_favorite(
    uuid: str, current_user: User = Depends(get_current_active_user)
) -> None:
    loc = await get_location(uuid)
    current_user.remove_favorite(loc)
    current_user.save()


@router.get("/{uuid}/review", response_model=List[Review])
async def get_reviews(uuid: str) -> List[Review]:
    loc = await get_location(uuid)
    return loc.reviews


@router.post("/{uuid}/review", response_model=Review)
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


@router.get("/{uuid}/review/{review_uuid}", response_model=Review)
async def get_review(uuid: str, review_uuid: str) -> Review:
    loc = await get_location(uuid)  # noqa
    rew = cast(Review, Review.get_by_uuid(review_uuid))
    if not rew:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The location with the uuid {uuid} does not exist!",
        )
    if loc != rew.location:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This review does not belong to this location!",
        )
    return rew


@router.delete("/{uuid}/review/{review_uuid}")
async def remove_review(
    uuid: str,
    review_uuid: str,
    current_user: User = Depends(get_current_active_user),
) -> None:
    rew = await get_review(uuid, review_uuid)
    if current_user != rew.writer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You did not create this review!",
        )
    rew.delete()


@router.patch("/{uuid}/review/{review_uuid}", response_model=Review)
async def update_review(
    uuid: str,
    review_uuid: str,
    rew_in: UpdateReviewSchema,
    current_user: User = Depends(get_current_active_user),
) -> Review:
    rew = await get_review(uuid, review_uuid)
    if current_user != rew.writer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You did not create this review!",
        )

    rew.update(**rew_in.dict())
    rew.save()
    return rew
