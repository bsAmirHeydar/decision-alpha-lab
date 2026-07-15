from pathlib import Path
import json
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[3]
m=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_12/CONTRACT_VALIDATION_MAP.JSON').read_text())
for pair in m['pairs']:
 s=json.loads((ROOT/pair['schema']).read_text());d=json.loads((ROOT/pair['document']).read_text());Draft202012Validator.check_schema(s);Draft202012Validator(s).validate(d)
print(f"V4-12 contracts validated: {len(m['pairs'])} document/schema pairs")
