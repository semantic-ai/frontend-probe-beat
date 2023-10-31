from typing import NamedTuple

from .sparql import SparqlConfig


class Config(NamedTuple):
    sparql = SparqlConfig()


config = Config()
