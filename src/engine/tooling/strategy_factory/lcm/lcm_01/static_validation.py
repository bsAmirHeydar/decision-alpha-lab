from __future__ import annotations
import json
from pathlib import Path
import jsonschema

def validate_registries(repo_root: Path) -> dict:
    schema_root=repo_root/'registry/history/lcm/lcm_01/schemas/v1'
    policy_root=repo_root/'registry/history/lcm/lcm_01/policies/v1'
    registry_root=repo_root/'registry/history/lcm/lcm_01/registries/v1'
    schemas=[]; errors=[]
    for p in sorted(schema_root.glob('*.json')):
        try: v=json.loads(p.read_text(encoding='utf-8')); jsonschema.Draft202012Validator.check_schema(v); schemas.append(p.name)
        except Exception as e: errors.append({'path':str(p),'error':str(e)})
    parsed=[]
    for p in sorted(list(policy_root.glob('*.json'))+list(registry_root.glob('*.json'))):
        try: json.loads(p.read_text(encoding='utf-8')); parsed.append(p.name)
        except Exception as e: errors.append({'path':str(p),'error':str(e)})
    return {'passed':not errors,'schema_count':len(schemas),'machine_contract_count':len(parsed),'errors':errors}
