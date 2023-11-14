from typing import NamedTuple

from .sparql import SparqlConfig
from .fastapi import FastApiConfig


class Config(NamedTuple):
    sparql = SparqlConfig()
    fastapi = FastApiConfig()


config = Config()
