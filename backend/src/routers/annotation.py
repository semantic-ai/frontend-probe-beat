import json
import logging

from fastapi import APIRouter, Depends, Query, Response, HTTPException

from ..config.iam import validate_user
from ..schemas.annotation import AnnotationResponse, AnnotationCreate
from ..services.annotation import AnnotationService


router = APIRouter(prefix="/api")


@router.get("/annotations")
def get_annotations(
    response: Response,
    range: str = Query(default="[0, 100]"),
    filter: str = Query(default="{}"),
    sort: str = Query(default='["id", "DESC"]'),
    user: None = Depends(validate_user),
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
    user: None = Depends(validate_user),
):
    try:
        result = AnnotationService().create(item)
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500)
    return result.handle()
