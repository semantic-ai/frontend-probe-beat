import json
from fastapi import APIRouter, Security, Query, Response

from ..schemas.annotation import (
    AnnotationResponse,
    AnnotationCreate,
)
from ..services.annotation import AnnotationService
from ..config.iam import validate_user

router = APIRouter(prefix="/api")


@router.get("/annotations", response_model=AnnotationResponse)
async def get_(
    response: Response,
    range: str = Query(default="[0, 100]"),
    filter: str = Query(default="{}"),
    sort: str = Query(default='["id", "DESC"]'),
    user: None = Security(dependency=validate_user, scopes=[]),
):
    start, stop = json.loads(range)
    filter = json.loads(filter)
    order = json.loads(sort)
    result = AnnotationService().get_all(filter, order)
    return result.handle(response)


@router.post("/annotations")
async def create_annotation(
    item: AnnotationCreate,
    user: None = Security(dependency=validate_user, scopes=[]),
):
    result = AnnotationService().create(item)
    return result.handle()
