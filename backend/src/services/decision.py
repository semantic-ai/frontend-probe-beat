from .main import SparkRequestHandler, AppService
from ..schemas.decision import (
    DecisionOverview,
    DecisionResponse,
    DecisionDetailed,
    Article,
)
from ..utils.service_result import ServiceResult
from ..enums import SparqlType


class DecisionService(AppService):
    def get_all(self, start: int, stop: int, filters: dict[str, any]) -> ServiceResult:
        decisions = DecisionCRUD().get_all(start, stop, filters)
        headers = self.list_headers(start, stop, decisions.total)
        return ServiceResult(decisions, headers=headers)

    def get_one(self, id: str) -> ServiceResult:
        decision = DecisionCRUD().get_one(self.decode_id(id))
        return ServiceResult(decision)


class DecisionCRUD(SparkRequestHandler):
    def __init__(self):
        super().__init__(SparqlType.DECISION)

    def get_all(
        self, start: int, stop: int, filters: dict[str, any]
    ) -> DecisionResponse:
        # Prepare filter
        filter_str = ""
        for source, value in filters.items():
            if source == "short_title":
                filter_str += (
                    'FILTER (CONTAINS(LCASE(STR(?short_title)), "{}" ))'.format(
                        str(value).lower()
                    )
                )
            else:
                filter_str += 'FILTER CONTAINS(?{}, "{}") '.format(source, str(value))

        # Get total decisions
        total_query_str = """
        PREFIX eli: <http://data.europa.eu/eli/ontology#>
        PREFIX besluit: <http://data.vlaanderen.be/ns/besluit#>

        SELECT (COUNT(*) AS ?count) WHERE {{
        ?_besluit a besluit:Besluit.
        OPTIONAL {{?_besluit eli:title_short ?short_title. }}
        FILTER (STRSTARTS(STR(?_besluit), "https://data"))
        {0}
        }}
        """.format(
            filter_str
        )
        total_decisions = int(
            self.query(total_query_str)["results"]["bindings"][0]["count"]["value"]
        )

        # Get decision page
        query_str = """
        PREFIX eli: <http://data.europa.eu/eli/ontology#>
        PREFIX besluit: <http://data.vlaanderen.be/ns/besluit#>
        PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?_besluit (SAMPLE(?short_title) as ?short_title)
        (IF(COUNT(?user) >= 1,"true", "false") AS ?user_annotated)
        WHERE {{
            ?_besluit a besluit:Besluit.
            OPTIONAL {{?_besluit eli:title_short ?short_title. }}
            OPTIONAL {{?_besluit ext:hasAnnotation / ext:withUser ?user . }}
            FILTER (!STRSTARTS(STR(?_besluit), "https://ebesluitvorming"))
            FILTER (!STRSTARTS(STR(?_besluit), "http://ebesluitvorming"))
            {0}
        }}
        GROUP BY ?_besluit
        LIMIT {1}
        OFFSET {2}
        """.format(
            filter_str, str(stop - start + 1), str(start)
        )
        decisions = self.query(query_str)["results"]["bindings"]
        decisions = [
            DecisionOverview(
                id=decision["_besluit"]["value"],  # .split("/")[-1]
                short_title=decision.get("short_title", {}).get("value", None),
                user_annotated=decision.get("user_annotated", {}).get("value", False),
            )
            for decision in decisions
        ]

        return DecisionResponse(decisions=decisions, total=total_decisions)

    def get_one(self, id: str) -> DecisionDetailed:
        query_str = """
        PREFIX eli: <http://data.europa.eu/eli/ontology#>
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX besluit: <http://data.vlaanderen.be/ns/besluit#>

        SELECT * WHERE {{
        VALUES ?_besluit {{ <{0}> }}
        ?_besluit prov:wasGeneratedBy ?_behandeling.
        ?_behandeling dct:subject ?_agendapunt.
        OPTIONAL {{?_besluit eli:description ?beschrijving.}}
        OPTIONAL {{?_besluit eli:title_short ?short_title.}}
        OPTIONAL {{?_besluit besluit:motivering ?motivering.}}
        OPTIONAL {{?_besluit eli:date_publication ?publicatiedatum.}}
        OPTIONAL {{?_besluit prov:wasDerivedFrom ?portal_link .}}
        }}
        """.format(
            id
        )
        decision = self.query(query_str)["results"]["bindings"][0]

        article_query_str = """
        PREFIX besluit: <http://data.vlaanderen.be/ns/besluit#>
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX eli: <http://data.europa.eu/eli/ontology#>
        SELECT * WHERE {{
        ?_besluit a besluit:Besluit.
        ?_besluit eli:has_part ?_artikel.
        OPTIONAL {{ ?_artikel eli:number ?number. }}
        OPTIONAL {{ ?_artikel prov:value ?waarde. }}
        FILTER (?_besluit = <{0}>)
        }}
        ORDER BY ?number
        """.format(
            id
        )
        articles = self.query(article_query_str)["results"]["bindings"]
        article_list = []
        for article in articles:
            article_list.append(
                Article(
                    id=article.get("_artikel", {}).get("value", None),
                    number=article.get("number", {}).get("value", None),
                    content=article.get("waarde", {}).get("value", None),
                )
            )

        return DecisionDetailed(
            id=id,
            short_title=decision.get("short_title", {}).get("value", None),
            description=decision.get("beschrijving", {}).get("value", None),
            motivation=decision.get("motivering", {}).get("value", None),
            portal_link=decision.get("portal_link", {}).get("value", None),
            articles=article_list,
        )
