import logging
import requests
import uuid
from datetime import datetime

from .main import SparkRequestHandler, AppService
from .taxonomy import TaxonomyCRUD
from ..schemas.annotation import (
    AnnotationResponse,
    AnnotationCreate,
    AnnotationOverview,
)
from ..utils.service_result import ServiceResult
from ..enums import SparqlType


class AnnotationService(AppService):
    def get_all(self, filter, order) -> ServiceResult:
        annotations = AnnotationCRUD().get_all(filter, order)
        headers = self.list_headers(
            0, 100, annotations.total
        )
        return ServiceResult(annotations, headers=headers)

    def create(self, item: AnnotationCreate) -> ServiceResult:
        annotation = AnnotationCRUD().create(
            decision_id=item.decision_id,
            taxonomy_id=item.taxonomy_id,
            labels=item.labels,
        )
        assert annotation
        return ServiceResult(annotation)


class AnnotationCRUD(SparkRequestHandler):
    def __init__(self):
        super().__init__(SparqlType.DECISION)

    def get_all(self, filter, order) -> AnnotationResponse:
        if "decision_id" not in filter.keys():
            return AnnotationResponse(annotations=[], total=0)

        decision_id = filter["decision_id"]
        # TODO: get user information if relevant
        query = """
        PREFIX besluit: <http://data.vlaanderen.be/ns/besluit#>
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX eli: <http://data.europa.eu/eli/ontology#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX ext:  <http://mu.semte.ch/vocabularies/ext/>

        SELECT * WHERE
        {{
            VALUES ?besluit {{<{}> }}
            ?besluit ext:hasAnnotation ?anno .
            ?anno  ext:creationDate ?date ; ext:withTaxonomy ?taxonomy_uri .
            OPTIONAL
            {{
                ?anno ext:withModel ?model_uri .
                OPTIONAL
                {{
                    SELECT * WHERE
                    {{
                        ?model_uri ext:modelCategory ?category;
                                ext:registeredMlflowModel ?mlflow_model;
                                ext:modelName ?model_name;
                                ext:mlflowLink ?mlflow_link;
                                ext:creationDate ?create_data .
                    }}
                }}
            }}
            OPTIONAL
            {{
                ?anno ext:withUser ?user_uri .
            #    {{
            #      SELECT * WHERE
            #      {{
            #      }}
            #    }}
            }}
            OPTIONAL
            {{
                SELECT DISTINCT ?anno  (GROUP_CONCAT(?taxonomy_node;separator="|") AS ?taxonomy_node_uris)
                 (GROUP_CONCAT(?score;separator="|") AS ?scores) WHERE
                {{
                    ?anno ext:hasLabel ?label_uri .
                    ?label_uri ext:hasScore ?score ; ext:isTaxonomy ?taxonomy_node .
                    FILTER (?score > 0.65)
                }} GROUP BY ?anno
            }}
        }}
        """.format(
            decision_id
        )

        annotations_info = self.query(query)["results"]["bindings"]

        annotations = []
        for annotation in annotations_info:
            id = annotation.get("anno", {}).get("value", "")
            taxonomy_uri = annotation.get("taxonomy_uri", {}).get("value", "")
            date = datetime.fromtimestamp(int(annotation["date"]["value"]))

            # Get annotator
            if "user_uri" in annotation.keys():
                annotator = annotation["user_uri"]["value"]
                user = True
            elif "model_uri" in annotation.keys():
                annotator = annotation["model_uri"]["value"]
                user = False
            else:
                continue

            labels = (
                annotation.get("taxonomy_node_uris", {}).get("value", "").split("|")
            )
            annotations.append(
                AnnotationOverview(
                    id=id,
                    taxonomy_id=taxonomy_uri,
                    decision_id=decision_id,
                    labels=labels,
                    date=date,
                    annotator=annotator,
                    user=user,
                )
            )

        annotations.sort(key=lambda x: x.date, reverse=True)

        return AnnotationResponse(annotations=annotations, total=len(annotations))

    def create(
        self, decision_id: str, taxonomy_id: str, labels: list[str]
    ) -> AnnotationOverview | None:
        assert len(labels) > 0
        annotation_uuid = str(uuid.uuid4())

        # Filter labels to only contain labels for this category
        taxonomy_labels = []
        for node_list in TaxonomyCRUD().get_one(taxonomy_id).tree.values():
            taxonomy_labels += [node["id"] for node in node_list]
        labels = [label for label in labels if label in taxonomy_labels]

        label_part_query = ""
        if len(labels) > 0:
            labels_uri = [f"<https://lblod.data.gift/concepts/ml2grow/label/{uuid.uuid4()}>" for _ in labels]
            labels_str = ", ".join(labels_uri)
            label_part_query = """
            <https://lblod.data.gift/concepts/ml2grow/annotations/{annotation_uuid}>
            ext:hasLabel {labels_str} . """.format(
                annotation_uuid=annotation_uuid, labels_str=labels_str
            )

            for i in range(len(labels)):
                label_uri = labels_uri[i]
                label_tax = labels[i]
                label_part_query += """{label_uri} ext:isTaxonomy <{label_tax}> .
                {label_uri} ext:hasScore 1.0 . """.format(
                    label_uri=label_uri, label_tax=label_tax
                )

        # TODO: possibility for non-hardcoded user in the future
        query = """
        PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>

        INSERT DATA {{
        GRAPH <http://mu.semte.ch/application/probe/user-annotations>
        {{
        <{decision_uri}> ext:hasAnnotation
        <https://lblod.data.gift/concepts/ml2grow/annotations/{annotation_uuid}> .
        <https://lblod.data.gift/concepts/ml2grow/annotations/{annotation_uuid}>
        ext:withTaxonomy <{taxonomy_uri}> .
        <https://lblod.data.gift/concepts/ml2grow/annotations/{annotation_uuid}>
        ext:creationDate {date_time} .
        <https://lblod.data.gift/concepts/ml2grow/annotations/{annotation_uuid}>
        ext:withUser
        <https://classifications.ghent.com/ml2grow/user/15e14840-0455-42f6-a5e6-1dde35d868e7> .
        {label_part_query}
        }}
        }}
        """.format(
            decision_uri=decision_id,
            annotation_uuid=annotation_uuid,
            taxonomy_uri=taxonomy_id,
            label_part_query=label_part_query,
            date_time=str(int(datetime.now().timestamp())),
        )

        result = self.query(query)
        if isinstance(result, requests.Response):
            logging.error(
                "Error when inserting:\nResponse status:{}\nContent: {}:".format(
                    str(result.status_code), str(result.content)
                )
            )
            return None

        return AnnotationOverview(
            id="https://lblod.data.gift/concepts/ml2grow/annotations/" + annotation_uuid,
            decision_id="",
            taxonomy_id="",
            labels=[],
            date=datetime.now(),
            annotator="https://classifications.ghent.com/ml2grow/user/15e14840-0455-42f6-a5e6-1dde35d868e7",
            user=True,
        )
