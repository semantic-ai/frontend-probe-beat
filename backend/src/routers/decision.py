import json
import logging
from fastapi import APIRouter, Security, Query, Response, HTTPException

from ..schemas.decision import DecisionResponse, DecisionDetailed
from ..services.decision import DecisionService

from ..config.iam import validate_user

router = APIRouter(prefix="/api")


@router.get("/decisions")
def get_decisions(
    response: Response,
    range: str = Query(default="[0, 999]"),
    filter: str = Query(default="{}"),
    user: None = Security(dependency=validate_user, scopes=[]),
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
    user: None = Security(dependency=validate_user, scopes=[]),
) -> DecisionDetailed:
    try:
        result = DecisionService().get_one(id)
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500)
    return result.handle()
