import json
from fastapi import APIRouter, Security, Query, Response

from ..schemas.decision import DecisionResponse, DecisionDetailed
from ..services.decision import DecisionService

from ..config.iam import validate_user

router = APIRouter(prefix="/api")


@router.get("/decisions", response_model=DecisionResponse)
async def get_decisions(
    response: Response,
    range: str = Query(default="[0, 999]"),
    filter: str = Query(default="{}"),
    user: None = Security(dependency=validate_user, scopes=[]),
):
    start, stop = json.loads(range)
    filters = json.loads(filter)
    result = DecisionService().get_all(start, stop, filters)
    return result.handle(response)


@router.get("/decisions/{id}", response_model=DecisionDetailed)
async def get_decision(
    id: str,
    user: None = Security(dependency=validate_user, scopes=[]),
):
    result = DecisionService().get_one(id)
    return result.handle()
