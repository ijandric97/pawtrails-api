from typing import List, cast

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends

from pawtrails.api.deps import get_current_active_user
from pawtrails.api.v0.routes.user import get_user_by_uuid
from pawtrails.models.pet import AddPetSchema, Pet, PetSchema, UpdatePetSchema
from pawtrails.models.user import User, UserSchema

router = APIRouter()


async def _check_ownership(user: User, pet: Pet) -> None:
    if user not in pet.owners:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"This user {user.username} does not own this pet!",
        )


@router.get("/", response_model=List[PetSchema])
async def get_pet_list() -> List[Pet]:
    return Pet.get_all()


@router.post("/", response_model=PetSchema)
async def add_pet(
    pet_in: AddPetSchema, current_user: User = Depends(get_current_active_user)
) -> Pet:
    pet = Pet(**pet_in.dict())
    pet.add_owner(current_user)
    pet.save()
    return pet


@router.get("/{uuid}", response_model=PetSchema)
async def get_pet(uuid: str) -> Pet:
    pet = cast(Pet, Pet.get_by_uuid(uuid))
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The pet with the uuid {uuid} does not exist!",
        )

    return pet


@router.delete("/{uuid}", response_model=None)
async def delete_pet(
    uuid: str, current_user: User = Depends(get_current_active_user)
) -> None:
    pet = await get_pet(uuid)
    await _check_ownership(current_user, pet)
    pet.delete()  # TODO: Perhaps we should just remove it from this owner


@router.patch("/{uuid}", response_model=PetSchema)
async def update_pet(
    pet_in: UpdatePetSchema,
    uuid: str,
    current_user: User = Depends(get_current_active_user),
) -> Pet:
    pet = await get_pet(uuid)

    # pet = Pet(**pet_in.dict())
    # pet.add_owner(current_user)
    # pet.save()
    # FIXME: Finish this plsss
    return pet


@router.get("/{uuid}/owner", response_model=List[UserSchema])
async def get_pet_owners(uuid: str) -> List[User]:
    pet = await get_pet(uuid)
    return pet.owners


@router.post("/{uuid}/owner", response_model=None)
async def add_pet_owner(
    uuid: str, user_uuid: str, current_user: User = Depends(get_current_active_user)
) -> None:
    pet = await get_pet(uuid)
    await _check_ownership(current_user, pet)
    user = await get_user_by_uuid(user_uuid)

    if not pet.add_owner(user):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="That user already owns this pet.",
        )


@router.delete("/{uuid}/owner", response_model=None)
async def remove_pet_owner(
    uuid: str, user_uuid: str, current_user: User = Depends(get_current_active_user)
) -> None:
    pet = await get_pet(uuid)
    await _check_ownership(current_user, pet)
    user = await get_user_by_uuid(user_uuid)

    if not pet.remove_owner(user):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="That user does not own this pet",
        )

    # All owners decided to abandon this pet, remove it from the database
    if not pet.owners:
        pet.delete()
