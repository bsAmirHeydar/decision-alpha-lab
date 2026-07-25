from tools.repository_paths import find_repository_root
from pathlib import Path
import json
from jsonschema import Draft202012Validator, FormatChecker

ROOT = find_repository_root(__file__)
SCHEMAS = ROOT / "schemas/legacy/strategy_factory/saed_v4_06"
EXAMPLES = ROOT / "examples/legacy/strategy_factory/saed_v4_06"
PAIRS = (
    ("institutional_treatment_dsl_registry.json", "treatment_dsl_registry.schema.json"),
    ("institutional_treatment_dsl_policy.json", "treatment_dsl_policy.schema.json"),
    ("institutional_capability_profile.json", "capability_profile.schema.json"),
    ("golden_treatment_program_source.json", "treatment_program_source.schema.json"),
    ("system_skip_program_source.json", "treatment_program_source.schema.json"),
    ("system_abstain_program_source.json", "treatment_program_source.schema.json"),
    ("golden_canonical_treatment_program.json", "canonical_treatment_program.schema.json"),
    ("golden_program_validation.json", "program_validation_result.schema.json"),
    ("golden_descriptor_binding.json", "descriptor_binding.schema.json"),
    ("golden_treatment_dsl_package.json", "treatment_dsl_package.schema.json"),
    ("golden_dsl_integrity_receipt.json", "dsl_integrity_receipt.schema.json"),
    ("golden_dsl_replay_receipt.json", "dsl_replay_receipt.schema.json"),
    ("golden_dsl_diff.json", "dsl_diff.schema.json"),
    ("golden_dsl_telemetry.json", "dsl_telemetry.schema.json"),
    ("golden_dsl_partition_manifest.json", "dsl_partition_manifest.schema.json"),
    ("golden_exposure_ledger.json", "exposure_ledger.schema.json"),
    ("golden_conformance_results.json", "conformance_results.schema.json"),
    ("conformance_vectors.json", "conformance_vectors.schema.json"),
    ("v4_06_to_v4_07_handoff.json", "v4_06_to_v4_07_handoff.schema.json"),
    ("schema_catalog.json", "schema_catalog.schema.json"),
)
schemas = sorted(SCHEMAS.glob("*.schema.json"))
if len(schemas) < 26:
    raise SystemExit("insufficient V4-06 schema catalog")
for path in schemas:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    if schema.get("additionalProperties") is not False:
        raise SystemExit(f"schema is not top-level closed: {path.relative_to(ROOT)}")
for example_name, schema_name in PAIRS:
    document = json.loads((EXAMPLES / example_name).read_text(encoding="utf-8"))
    schema = json.loads((SCHEMAS / schema_name).read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(document), key=lambda e: list(e.absolute_path))
    if errors:
        first=errors[0]
        location="/".join(str(x) for x in first.absolute_path)
        raise SystemExit(f"{example_name}@{location}: {first.message}")
# Validate every source component against the standalone component contract.
component_schema=json.loads((SCHEMAS/'program_component_source.schema.json').read_text(encoding='utf-8'))
for source_name in ('golden_treatment_program_source.json','system_skip_program_source.json','system_abstain_program_source.json'):
    source=json.loads((EXAMPLES/source_name).read_text(encoding='utf-8'))
    for index, component in enumerate(source['components']):
        errors=list(Draft202012Validator(component_schema).iter_errors(component))
        if errors:
            raise SystemExit(f"{source_name}/components/{index}: {errors[0].message}")
print(f"validated {len(schemas)} closed schemas and {len(PAIRS)} golden contracts")
