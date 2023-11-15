import json
import logging
from fastapi import APIRouter, Security, Query, Response, HTTPException

from ..schemas.taxonomy import TaxonomyResponse, TaxonomyDetailed
from ..services.taxonomy import TaxonomyService
from ..config.iam import validate_user


router = APIRouter(prefix="/api")


@router.get("/taxonomies")
def get_taxonomies(
    response: Response,
    filter: str = Query(default="{}"),
    user: None = Security(dependency=validate_user, scopes=[]),
) -> TaxonomyResponse:
    filters = json.loads(filter)
    try:
        result = TaxonomyService().get_all(filters)
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500)
    return result.handle(response)


@router.get("/taxonomies/{id}")
def get_taxonomy(
    id: str,
    user: None = Security(dependency=validate_user, scopes=[]),
) -> TaxonomyDetailed:
    try:
        result = TaxonomyService().get_one(id)
    except Exception as ex:
        logging.error(ex)
        raise HTTPException(status_code=500)
    return result.handle()
