from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from pawtrails.api.deps import get_current_active_user, get_current_user
from pawtrails.api.v0.routes.user import get_user_by_uuid
from pawtrails.models.location import Location, LocationSchema
from pawtrails.models.pet import Pet, PetSchema
from pawtrails.models.review import Review, ReviewSchema
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

    current_user.save()
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

    current_user.save()
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


@router.get("/locations", response_model=List[LocationSchema])
async def get_locations(
    current_user: User = Depends(get_current_user),
) -> List[Location]:
    return current_user.locations


@router.get("/favorites", response_model=List[LocationSchema])
async def get_favorites(
    current_user: User = Depends(get_current_user),
) -> List[Location]:
    return current_user.favorites


@router.get("/reviews", response_model=List[ReviewSchema])
async def get_reviews(
    current_user: User = Depends(get_current_user),
) -> List[Review]:
    return current_user.reviews
