import json
import logging

from fastapi import APIRouter, Depends, Query, Response, HTTPException

from ..config.iam import validate_user
from ..schemas.decision import DecisionResponse, DecisionDetailed
from ..services.decision import DecisionService


router = APIRouter(prefix="/api")


@router.get("/decisions")
def get_decisions(
    response: Response,
    range: str = Query(default="[0, 999]"),
    filter: str = Query(default="{}"),
    user: None = Depends(validate_user),
) -> DecisionResponse:
    start, stop = json.loads(range)
    filters = json.loads(filter)
    try:
        result = DecisionService().get_all(start, stop, filters)
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500)
    return result.handle(response)


@router.get("/decisions/{id}", response_model=DecisionDetailed)
def get_decision(
    id: str,
    user: None = Depends(validate_user),
) -> DecisionDetailed:
    try:
        result = DecisionService().get_one(id)
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500)
    return result.handle()
