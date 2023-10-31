import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

from ..config import config
from ..enums import SparqlType, SparqlAuthType


class AppService:
    @staticmethod
    def list_headers(start: int, stop: int, total: int) -> dict[str, str]:
        return {"Content-Range": "posts {0}-{1}/{2}".format(start, stop, total)}

    @staticmethod
    def decode_id(id: str) -> str:
        # Replace \ with "Forwardslash" (frontend switches them to encode uri)
        return id.replace("Forwardslash", "/")


class SparkRequestHandler:
    HEADERS = {"accept": "application/sparql-results+json,*/*;q=0.9"}

    def __init__(self, sparql_type: SparqlType):
        self.config = config

        match self.config.sparql.auth_type:
            case SparqlAuthType.NONE:
                self.auth = None
            case SparqlAuthType.BASIC:
                self.auth = HTTPBasicAuth(
                    self.config.sparql.auth_username, self.config.sparql.auth_password
                )
            case SparqlAuthType.DIGEST:
                self.auth = HTTPDigestAuth(
                    self.config.sparql.auth_username, self.config.sparql.auth_password
                )

        match sparql_type:
            case SparqlType.DECISION:
                self.endpoint = self.config.sparql.decision_endpoint
            case SparqlType.TAXONOMY:
                self.endpoint = self.config.sparql.taxonomy_endpoint

    def query(self, query: str):
        response = requests.post(
            url=self.endpoint,
            data={"query": query},
            headers=self.HEADERS,
            auth=self.auth,
        )

        if not response.ok:
            print(response.text)

        return response.json()
