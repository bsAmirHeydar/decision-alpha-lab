from __future__ import annotations
import json,re
from pathlib import Path
from .schema_validation import validate_schema_file
from .policies import FLEET_STATUSES,CLOSURE_STATES,ALLOWED_REOPEN_ACTIONS,FORBIDDEN_ACTIONS
def validate_registry(root:Path)->dict:
    base=root/'registry/history/acl/acl_15'; errors=[]
    schemas=list((base/'schemas/v1').glob('*.json')); policies=list((base/'policies/v1').glob('*.json'))
    for p in schemas: errors.extend([f'{p.name}:{e}' for e in validate_schema_file(p)])
    for p in policies:
        try: json.loads(p.read_text(encoding='utf-8'))
        except Exception as e: errors.append(f'{p.name}:{e}')
    if len(schemas)<20: errors.append('SCHEMA_COUNT_LOW')
    if len(policies)<20: errors.append('POLICY_COUNT_LOW')
    mql=root/'mql5/legacy/strategy_factory_lab/Include/AlphaLab/ACL_OS/ACL15'
    forbidden=re.compile(r'(OrderSend|CTrade|PositionOpen|WebRequest|Buy\s*\(|Sell\s*\()')
    hits=[]
    for p in mql.glob('*.mqh'):
        if forbidden.search(p.read_text(encoding='utf-8')): hits.append(p.name)
    if hits: errors.append('MQL5_FORBIDDEN_API:'+','.join(hits))
    return {'passed':not errors,'errors':errors,'schema_count':len(schemas),'policy_count':len(policies),'mql5_forbidden_hits':hits,'fleet_status_count':len(FLEET_STATUSES),'closure_state_count':len(CLOSURE_STATES),'allowed_reopen_action_count':len(ALLOWED_REOPEN_ACTIONS),'forbidden_action_count':len(FORBIDDEN_ACTIONS)}
