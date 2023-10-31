from pydantic import BaseModel


class TaxonomyOverview(BaseModel):
    id: str
    name: str


class TaxonomyResponse(BaseModel):
    taxonomies: list[TaxonomyOverview]
    total: int


class TaxonomyDetailed(BaseModel):
    id: str
    name: str
    tree: dict[str, list[dict[str, str]]]
