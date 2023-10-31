from enum import Enum


class SparqlType(Enum):
    DECISION = 1
    TAXONOMY = 2


class SparqlAuthType(Enum):
    NONE = "none"
    BASIC = "basic"
    DIGEST = "digest"
