from fastapi import APIRouter, HTTPException

from app.models.user import User
from app.schemas.user import RegisterUserSchema, UserSchema

router = APIRouter()


@router.post("/register", response_model=UserSchema)
def register(*, user_in: RegisterUserSchema):
    user = User.get_by_email(user_in.email) or User.get_by_username(user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username/email already exists in the system.",
        )

    user = User(**user_in.dict())
    user.save()

    return user
