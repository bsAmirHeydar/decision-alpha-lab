from __future__ import annotations
from tools.repository_paths import find_repository_root

import json
from pathlib import Path

import jsonschema
import pytest

ROOT = find_repository_root(__file__)
EXAMPLES = ROOT / "examples/legacy/strategy_factory/saed_v4_25"
ARTIFACTS = ROOT / "releases/history/strategy_factory/artifacts/saed_v4_25"
SCHEMAS = ROOT / "schemas/legacy/strategy_factory/saed_v4_25"
PAIRS = []
for directory in (EXAMPLES, ARTIFACTS):
    for instance in sorted(directory.glob("*.JSON")):
        schema = SCHEMAS / f"{instance.stem}.SCHEMA.JSON"
        PAIRS.append((instance, schema))


@pytest.mark.parametrize("instance,schema", PAIRS, ids=[pair[0].name for pair in PAIRS])
def test_closed_schema_pair(instance, schema):
    assert schema.is_file()
    instance_value = json.loads(instance.read_text(encoding="utf-8"))
    schema_value = json.loads(schema.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema_value)
    jsonschema.validate(instance_value, schema_value, cls=jsonschema.Draft202012Validator)


@pytest.mark.parametrize("schema", sorted(SCHEMAS.glob("*.SCHEMA.JSON")), ids=lambda path: path.name)
def test_all_object_schemas_are_closed(schema):
    value = json.loads(schema.read_text(encoding="utf-8"))
    def visit(node):
        if isinstance(node, dict):
            if node.get("type") == "object":
                assert node.get("additionalProperties") is False
            for child in node.values():
                visit(child)
        elif isinstance(node, list):
            for child in node:
                visit(child)
    visit(value)
