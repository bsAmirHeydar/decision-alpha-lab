from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
def validate_registry(root: Path) -> dict:
    errors=[]; schemas=list((root/'registry/acl_os/acl_11/schemas/v1').glob('*.json')); policies=list((root/'registry/acl_os/acl_11/policies/v1').glob('*.json'))
    for p in schemas:
        try: Draft202012Validator.check_schema(json.loads(p.read_text(encoding='utf-8')))
        except Exception as exc: errors.append(f'{p}:{exc}')
    for p in policies:
        try:
            v=json.loads(p.read_text(encoding='utf-8')); assert isinstance(v,dict)
        except Exception as exc: errors.append(f'{p}:{exc}')
    forbidden=['OrderSend(','CTrade','PositionOpen(','WebRequest(','Buy(','Sell(']
    hits=[]
    for p in (root/'lab/11_strategy_factory/mql5/Include/AlphaLab/ACL_OS/ACL11').glob('*'):
        if p.is_file():
            text=p.read_text(encoding='utf-8',errors='ignore')
            for token in forbidden:
                if token in text: hits.append(f'{p.name}:{token}')
    return {'passed':not errors and not hits,'schema_count':len(schemas),'policy_count':len(policies),'errors':errors,'forbidden_mql5_hits':hits}
