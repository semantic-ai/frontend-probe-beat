from pydantic import BaseModel


class DecisionOverview(BaseModel):
    id: str
    short_title: str | None
    user_annotated: bool


class DecisionResponse(BaseModel):
    decisions: list[DecisionOverview]
    total: int


class Article(BaseModel):
    id: str
    number: str
    content: str


class DecisionDetailed(BaseModel):
    id: str
    short_title: str | None
    description: str | None
    motivation: str | None
    portal_link: str | None
    articles: list[Article]
