import json
from pathlib import Path
import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[2]
FILES = sorted((ROOT / "schemas/v3").glob("qualification_*.schema.json"))


def test_i18_schema_inventory_is_complete_and_closed():
    assert len(FILES) >= 24
    for path in FILES:
        schema = json.loads(path.read_text())
        jsonschema.Draft202012Validator.check_schema(schema)
        assert schema["additionalProperties"] is False


@pytest.mark.parametrize("path", FILES)
def test_schema_accepts_minimum_identity(path):
    schema = json.loads(path.read_text())
    instance = {"schema_version": "1.0.0", "artifact_id": "x", "artifact_hash": "a" * 64}
    jsonschema.validate(instance, schema)
