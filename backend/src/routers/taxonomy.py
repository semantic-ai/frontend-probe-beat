import json
from fastapi import APIRouter, Security, Query, Response

from ..schemas.taxonomy import TaxonomyResponse, TaxonomyDetailed
from ..services.taxonomy import TaxonomyService
from ..config.iam import validate_user


router = APIRouter(prefix="/api")


@router.get("/taxonomies", response_model=TaxonomyResponse)
async def get_taxonomies(
    response: Response,
    filter: str = Query(default="{}"),
    user: None = Security(dependency=validate_user, scopes=[]),
):
    filters = json.loads(filter)
    result = TaxonomyService().get_all(filters)
    return result.handle(response)


@router.get("/taxonomies/{id}", response_model=TaxonomyDetailed)
async def get_taxonomy(
    id: str,
    user: None = Security(dependency=validate_user, scopes=[]),
):
    result = TaxonomyService().get_one(id)
    return result.handle()
