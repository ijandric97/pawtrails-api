from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class RegisterUserSchema(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserSchema(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True
