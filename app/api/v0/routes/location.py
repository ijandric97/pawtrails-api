from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_locations() -> None:
    pass


@router.post("/")
async def add_location() -> None:
    pass


@router.get("/{uuid}")
async def get_location(uuid: str) -> None:
    pass


@router.delete("/{uuid}")
async def remove_location(uuid: str) -> None:
    pass


@router.patch("/{uuid}")
async def update_location(uuid: str) -> None:
    pass


@router.get("/{uuid}/review")
async def get_reviews(uuid: str) -> None:
    pass


@router.post("/{uuid}/review")
async def add_review(uuid: str) -> None:
    pass


@router.delete("/{uuid}/review/{review_uuid}")
async def remove_review(uuid: str) -> None:
    pass


@router.patch("/{uuid}/review/{review_uuid}")
async def update_review(uuid: str) -> None:
    pass
