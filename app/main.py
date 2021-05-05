import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v0.api import api_router
from app.core.settings import settings

app = FastAPI(
    title="PawTrails",
    description="A Web API for the PawTrails Application",
    version="1.0.0",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_PREFIX)

# This line is necessary for debugging the application using VSCode
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
