from .main import SparkRequestHandler, AppService
from ..schemas.taxonomy import TaxonomyOverview, TaxonomyResponse, TaxonomyDetailed
from ..utils.service_result import ServiceResult
from ..enums import SparqlType


class TaxonomyService(AppService):
    def get_all(self, filter: dict[str, str] = {}) -> ServiceResult:
        taxonomies = TaxonomyCRUD().get_all(filter)
        headers = self.list_headers(
            0, 100, taxonomies.total
        )
        return ServiceResult(taxonomies, headers=headers)

    def get_one(self, id: str) -> ServiceResult:
        taxonomy = TaxonomyCRUD().get_one(self.decode_id(id))
        return ServiceResult(taxonomy)


class TaxonomyCRUD(SparkRequestHandler):
    def __init__(self):
        super().__init__(SparqlType.TAXONOMY)

    def get_all(self, filter: dict[str, str] = {}) -> TaxonomyResponse:
        query = """
        PREFIX void: <http://rdfs.org/ns/void#>

        SELECT ?vocabulary
        WHERE {
        <http://stad.gent/id/datasets/probe_taxonomies> void:vocabulary ?vocabulary
        }
        """
        taxonomies = []
        result = self.query(query)["results"]["bindings"]
        for r in result:
            uri = r.get("vocabulary", {}).get("value", "")
            if uri == "":
                continue
            # Filter on id
            if "id" in filter.keys() and uri != filter["id"]:
                continue
            name = uri.split("/")[-1]
            taxonomies.append(TaxonomyOverview(id=uri, name=name))

        return TaxonomyResponse(taxonomies=taxonomies, total=len(taxonomies))

    def get_one(self, id: str) -> TaxonomyDetailed:
        empty_query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        SELECT DISTINCT ?concept ?label ?broaderConcept ?broaderConceptLabel
        WHERE {{
        ?concept a skos:Concept ;
            skos:prefLabel ?label ;
            skos:inScheme <{}> .
        OPTIONAL {{
            ?concept skos:broader ?broaderConcept .
            ?broaderConcept skos:prefLabel ?broaderConceptLabel .
        }}
        }}
        ORDER BY ?broaderConceptLabel ?concept
        """
        start_query = empty_query.format(id)
        labels = self.query(start_query)["results"]["bindings"]

        tree_dict = {}
        for label in labels:
            label_id = label.get("concept", {}).get("value", "")
            label_name = label.get("label", {}).get("value", "")
            label_parent_id = label.get("broaderConcept", {}).get("value", "")
            if label_parent_id == "":
                label_parent_id = "top_level"

            tree_dict[label_parent_id] = tree_dict.get(label_parent_id, []) + [
                {"id": label_id, "name": label_name}
            ]

        # Check if top level domain is one node, remove and make toplevel second layer
        if len(tree_dict["top_level"]) == 1:
            label = tree_dict["top_level"][0]["id"]
            tree_dict["top_level"] = tree_dict[label]
            del tree_dict[label]

        return TaxonomyDetailed(id=id, name=id.split("/")[-1], tree=tree_dict)
