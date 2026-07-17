from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[3]
EX = ROOT / "lab/11_strategy_factory/examples/saed_v4_29"
AR = ROOT / "lab/11_strategy_factory/artifacts/saed_v4_29"
SC = ROOT / "lab/11_strategy_factory/schemas/saed_v4_29"


def schema(value):
    if isinstance(value, bool):
        return {"type": "boolean"}
    if isinstance(value, int):
        return {"type": "integer"}
    if isinstance(value, float):
        return {"type": "number"}
    if isinstance(value, str):
        return {"type": "string"}
    if isinstance(value, list):
        return {"type": "array", "items": schema(value[0]) if value else {}}
    if isinstance(value, dict):
        return {
            "type": "object",
            "additionalProperties": False,
            "properties": {key: schema(item) for key, item in sorted(value.items())},
            "required": sorted(value),
        }
    if value is None:
        return {"type": "null"}
    raise TypeError(type(value))


SC.mkdir(parents=True, exist_ok=True)
for path in sorted(EX.glob("*.JSON")) + sorted(AR.glob("*.JSON")):
    payload = schema(json.loads(path.read_text(encoding="utf-8")))
    payload = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://decision-alpha-lab.local/schemas/saed_v4_29/{path.stem}.schema.json",
        **payload,
    }
    (SC / (path.stem + ".SCHEMA.JSON")).write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
print(f"V4-29 schemas generated: {len(list(SC.glob('*.SCHEMA.JSON')))}")
