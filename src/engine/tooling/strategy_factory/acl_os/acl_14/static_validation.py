from __future__ import annotations
import json,re
from pathlib import Path
from jsonschema import Draft202012Validator
def validate_registry(root:Path)->dict:
    errors=[]; schema_count=policy_count=mql_count=0
    for p in sorted((root/'registry/acl_os/acl_14/schemas/v1').glob('*.json')):
        try: Draft202012Validator.check_schema(json.loads(p.read_text(encoding='utf-8'))); schema_count+=1
        except Exception as e: errors.append(f'SCHEMA:{p.name}:{e}')
    for p in sorted((root/'registry/acl_os/acl_14/policies/v1').glob('*.json')):
        try:
            v=json.loads(p.read_text(encoding='utf-8'))
            if not isinstance(v,dict) or not v.get('policy_id'): raise ValueError('policy_id missing')
            policy_count+=1
        except Exception as e: errors.append(f'POLICY:{p.name}:{e}')
    forbidden=re.compile(r'\b(OrderSend|CTrade|PositionOpen|WebRequest|Buy|Sell)\b')
    for p in sorted((root/'mql5/legacy/strategy_factory_lab/Include/AlphaLab/ACL_OS/ACL14').glob('*')):
        if p.is_file():
            mql_count+=1
            if forbidden.search(p.read_text(encoding='utf-8')): errors.append(f'FORBIDDEN_MQL5_API:{p.name}')
    return {'passed':not errors,'errors':errors,'schema_count':schema_count,'policy_count':policy_count,'mql5_file_count':mql_count}
