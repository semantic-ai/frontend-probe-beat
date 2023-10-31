from pydantic import BaseModel
from datetime import datetime


class AnnotationOverview(BaseModel):
    id: str
    decision_id: str
    taxonomy_id: str
    labels: list[str]
    date: datetime
    annotator: str | None
    user: bool


class AnnotationResponse(BaseModel):
    annotations: list[AnnotationOverview]
    total: int


class AnnotationCreate(BaseModel):
    decision_id: str
    taxonomy_id: str
    labels: list[str]
