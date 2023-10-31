from .base import Settings
from ..enums import SparqlAuthType


class SparqlConfig(Settings):
    decision_endpoint: str
    taxonomy_endpoint: str
    auth_type: SparqlAuthType = SparqlAuthType.NONE
    auth_username: str = ""
    auth_password: str = ""

    class Config:
        env_prefix = "sparql_"
