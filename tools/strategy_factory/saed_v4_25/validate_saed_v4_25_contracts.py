from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/strategy_factory/saed_v4_25"))
from _schema_validator import closed_objects, validate

examples = ROOT / "lab/11_strategy_factory/examples/saed_v4_25"
artifacts = ROOT / "lab/11_strategy_factory/artifacts/saed_v4_25"
schemas = ROOT / "lab/11_strategy_factory/schemas/saed_v4_25"
pairs = []
for directory in (examples, artifacts):
    for instance in sorted(directory.glob("*.JSON")):
        schema = schemas / f"{instance.stem}.SCHEMA.JSON"
        assert schema.is_file(), schema
        validate(instance, schema)
        value = json.loads(schema.read_text(encoding="utf-8"))
        assert closed_objects(value), schema
        assert value["x-phase"] == "SAED_V4_25"
        assert value["x-authority"] == "research-only-nonproduction"
        pairs.append((instance, schema))
assert len(pairs) == 36, len(pairs)
assert len(list(schemas.glob("*.SCHEMA.JSON"))) == len(pairs)
print(f"V4-25 contract validation passed: {len(pairs)} closed schema pairs")
