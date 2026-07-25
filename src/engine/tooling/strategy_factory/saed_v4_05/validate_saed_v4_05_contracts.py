from tools.repository_paths import find_repository_root
from pathlib import Path
import json

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

schemas = sorted(SCHEMAS.glob("*.schema.json"))
if len(schemas) < 20:
    raise SystemExit("insufficient V4-05 schema catalog")
for path in schemas:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    if schema.get("additionalProperties") is not False:
        raise SystemExit(f"schema is not closed: {path.relative_to(ROOT)}")
for example_name, schema_name in PAIRS:
    document = json.loads((EXAMPLES / example_name).read_text(encoding="utf-8"))
    schema = json.loads((SCHEMAS / schema_name).read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(document),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        raise SystemExit(f"{example_name}: {errors[0].message}")
print(f"validated {len(schemas)} closed schemas and {len(PAIRS)} golden contracts")
