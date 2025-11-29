from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/ping")
async def get_ping() -> dict[str, str]:
    """Healthcheck endpoint used to verify the service is up."""
    return {"message": "pong"}
