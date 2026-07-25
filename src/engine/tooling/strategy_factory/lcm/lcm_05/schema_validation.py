import json
from jsonschema import Draft202012Validator
def validate(repo_root):
    base=repo_root/'registry/legacy_context_migration/lcm_05/schemas/v1';count=0
    for p in sorted(base.glob('*.schema.json')):Draft202012Validator.check_schema(json.loads(p.read_text(encoding='utf-8')));count+=1
    return {"passed":True,"schema_count":count}
