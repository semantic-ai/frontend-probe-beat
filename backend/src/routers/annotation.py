import json
import logging
from fastapi import APIRouter, Security, Query, Response, HTTPException

from ..schemas.annotation import (
    AnnotationResponse,
    AnnotationCreate,
)
from ..services.annotation import AnnotationService
from ..config.iam import validate_user

router = APIRouter(prefix="/api")


@router.get("/annotations")
def get_annotations(
    response: Response,
    range: str = Query(default="[0, 100]"),
    filter: str = Query(default="{}"),
    sort: str = Query(default='["id", "DESC"]'),
    user: None = Security(dependency=validate_user, scopes=[]),
) -> AnnotationResponse:
    start, stop = json.loads(range)
    filter = json.loads(filter)
    order = json.loads(sort)
    try:
        result = AnnotationService().get_all(filter, order)
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500)
    return result.handle(response)


@router.post("/annotations")
def create_annotation(
    item: AnnotationCreate,
    user: None = Security(dependency=validate_user, scopes=[]),
):
    try:
        result = AnnotationService().create(item)
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500)
    return result.handle()
