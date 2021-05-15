from fastapi import APIRouter

from app.api.v0.routes import follow, login, user

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(follow.router, prefix="/follow", tags=["follow"])
