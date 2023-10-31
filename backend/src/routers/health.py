from fastapi import APIRouter, Response


router = APIRouter(prefix="/api")


@router.get("/health")
async def health():
    return Response(status_code=200)
