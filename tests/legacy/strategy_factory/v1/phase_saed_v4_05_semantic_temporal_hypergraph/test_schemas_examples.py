from tools.repository_paths import find_repository_root
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = find_repository_root(__file__)
SCHEMAS = ROOT / "schemas/legacy/strategy_factory/saed_v4_05"
EXAMPLES = ROOT / "examples/legacy/strategy_factory/saed_v4_05"


PAIRS = (
    ("institutional_semantic_registry.json", "semantic_registry.schema.json"),
    ("institutional_graph_policy.json", "graph_build_policy.schema.json"),
    ("golden_semantic_temporal_hypergraph.json", "semantic_temporal_hypergraph.schema.json"),
    ("golden_graph_integrity_receipt.json", "graph_integrity_receipt.schema.json"),
    ("golden_graph_replay_receipt.json", "graph_replay_receipt.schema.json"),
    ("golden_incidence_projection.json", "graph_projection.schema.json"),
    ("golden_partition_manifest.json", "partition_manifest.schema.json"),
    ("golden_hypergraph_telemetry.json", "hypergraph_telemetry.schema.json"),
    ("golden_graph_query.json", "graph_query.schema.json"),
    ("golden_graph_query_result.json", "graph_query_result.schema.json"),
    ("v4_05_to_v4_06_handoff.json", "v4_05_to_v4_06_handoff.schema.json"),
)


def test_all_schemas_are_closed_and_valid():
    schemas = list(SCHEMAS.glob("*.schema.json"))
    assert len(schemas) >= 20
    for path in schemas:
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        assert schema["additionalProperties"] is False


def test_golden_examples_validate_against_closed_contracts():
    for example_name, schema_name in PAIRS:
        document = json.loads((EXAMPLES / example_name).read_text(encoding="utf-8"))
        schema = json.loads((SCHEMAS / schema_name).read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(document))
        assert not errors, f"{example_name}: {[error.message for error in errors[:5]]}"


def test_negative_examples_are_explicitly_classified():
    negatives = list((EXAMPLES / "negative").glob("*.json"))
    assert len(negatives) >= 6
    for path in negatives:
        document = json.loads(path.read_text(encoding="utf-8"))
        assert document["expected"] == "reject"
        assert document["mutation"]
