import json
from pathlib import Path

import jsonschema
from referencing import Registry, Resource

from fp_i02_kernel.canonical import canonical_value
from fp_i02_kernel.golden import golden_bundle, golden_candidate, golden_confirmation, golden_hunt, golden_manifest, golden_quota_key, golden_reference_key, golden_signal, golden_window_key, golden_ww

ROOT = Path(__file__).resolve().parents[5]
SCHEMA_ROOT = ROOT / "lab/10_infrastructure/EXP0019_faerie_protocol/phase_i02/schemas"


def load(name):
    return json.loads((SCHEMA_ROOT / f"{name}.schema.json").read_text())


def resolver_registry():
    resources = []
    for path in SCHEMA_ROOT.glob("*.schema.json"):
        schema = json.loads(path.read_text())
        resources.append((schema["$id"], Resource.from_contents(schema)))
    return Registry().with_resources(resources)


def validate(name, value):
    schema = load(name)
    registry = resolver_registry()
    jsonschema.Draft202012Validator(schema, registry=registry).validate(canonical_value(value))


def test_all_public_schemas_are_closed_draft_2020_12():
    paths = sorted(SCHEMA_ROOT.glob("*.schema.json"))
    assert len(paths) == 18
    for path in paths:
        schema = json.loads(path.read_text())
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema["type"] == "object"
        assert schema["additionalProperties"] is False
        assert schema["required"]
        assert set(schema["required"]) <= set(schema["properties"])


def test_golden_contracts_validate_against_schemas():
    validate("fp_i02_symbol_pair", golden_manifest().pair)
    validate("fp_i02_window_key", golden_window_key())
    validate("fp_i02_reference_side_key", golden_reference_key())
    validate("fp_i02_hunt_fact", golden_hunt())
    validate("fp_i02_divergence_candidate", golden_candidate())
    validate("fp_i02_confirmation_event", golden_confirmation())
    validate("fp_i02_confirmed_signal", golden_signal())
    validate("fp_i02_ww_context_record", golden_ww())
    validate("fp_i02_quota_key", golden_quota_key())
    validate("fp_i02_semantic_configuration", golden_bundle().semantic)
    validate("fp_i02_projection_configuration", golden_bundle().projection)
    validate("fp_i02_context_manifest", golden_manifest())


def test_schema_rejects_unknown_property():
    payload = canonical_value(golden_manifest())
    payload["unknown"] = True
    with __import__('pytest').raises(jsonschema.ValidationError):
        validate("fp_i02_context_manifest", payload)


def test_schema_rejects_unknown_relation_enum():
    payload = canonical_value(golden_candidate())
    payload["relation"] = "AX"
    with __import__('pytest').raises(jsonschema.ValidationError):
        validate("fp_i02_divergence_candidate", payload)
