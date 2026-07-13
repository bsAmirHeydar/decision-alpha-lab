import json
from dataclasses import asdict
from pathlib import Path

import jsonschema
from referencing import Registry, Resource

from strategy_factory_experiments_v3.canonical import canonical_value
from strategy_factory_experiments_v3.compiler import ExperimentDagCompiler
from strategy_factory_experiments_v3.golden import golden_declaration
from strategy_factory_experiments_v3.registry import SearchRegistry

ROOT = Path(__file__).resolve().parents[4]
SCHEMA_ROOT = ROOT / "lab" / "11_strategy_factory" / "schemas" / "v3"


def schemas():
    items = {}
    for path in sorted(SCHEMA_ROOT.glob("experiment_*.schema.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        items[payload["$id"]] = payload
        items[path.name] = payload
        items[f"https://decision-alpha-lab.local/schemas/v3/{path.name}"] = payload
    return items


def schema_registry(store):
    resources = []
    seen = set()
    for payload in store.values():
        uri = payload["$id"]
        if uri not in seen:
            resources.append((uri, Resource.from_contents(payload)))
            seen.add(uri)
    return Registry().with_resources(resources)


def validate(name, instance):
    store = schemas()
    schema = store[f"https://decision-alpha-lab.local/schemas/v3/{name}.schema.json"]
    jsonschema.Draft202012Validator(schema, registry=schema_registry(store)).validate(canonical_value(instance))


def test_all_i11_schemas_are_closed_described_and_parseable():
    paths = sorted(SCHEMA_ROOT.glob("experiment_*.schema.json"))
    assert len(paths) == 24
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert payload["additionalProperties"] is False
        assert payload["description"].strip()
        jsonschema.Draft202012Validator.check_schema(payload)


def test_declaration_manifest_and_registry_validate_against_public_schemas():
    declaration = golden_declaration()
    manifest = ExperimentDagCompiler().compile(declaration)
    registry = SearchRegistry().freeze().snapshot()
    validate("experiment_declaration", declaration)
    validate("experiment_manifest", manifest)
    validate("experiment_search_registry_snapshot", registry)


def test_schema_rejects_unknown_top_level_property():
    declaration = canonical_value(golden_declaration())
    declaration["unknown_behavior"] = True
    store = schemas()
    schema = store["https://decision-alpha-lab.local/schemas/v3/experiment_declaration.schema.json"]
    try:
        jsonschema.Draft202012Validator(schema, registry=schema_registry(store)).validate(declaration)
    except jsonschema.ValidationError:
        pass
    else:
        raise AssertionError("closed schema accepted unknown property")
