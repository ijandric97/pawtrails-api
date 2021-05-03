from fastapi import APIRouter

from app.api.v0.routes import login, users

# Declare our API Router and add routes to it
api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
