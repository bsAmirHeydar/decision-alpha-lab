from tools.repository_paths import find_repository_root
from pathlib import Path
import json
from jsonschema import Draft202012Validator
ROOT=find_repository_root(__file__)
m=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_11/CONTRACT_VALIDATION_MAP.JSON').read_text())
for pair in m['pairs']:
 schema=json.loads((ROOT/pair['schema']).read_text());doc=json.loads((ROOT/pair['document']).read_text());Draft202012Validator.check_schema(schema);Draft202012Validator(schema).validate(doc)
print(f"V4-11 contracts validated: {m['pair_count']} document/schema pairs")
