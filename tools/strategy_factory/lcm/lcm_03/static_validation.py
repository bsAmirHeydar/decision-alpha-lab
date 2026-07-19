from __future__ import annotations
import json,re
from pathlib import Path
from .schema_validation import validate_schemas

def run(repo_root: Path):
    schema_count=validate_schemas(repo_root/'registry/legacy_context_migration/lcm_03/schemas/v1')
    policies=list((repo_root/'registry/legacy_context_migration/lcm_03/policies/v1').glob('*.json'))
    for p in policies: json.loads(p.read_text(encoding='utf-8'))
    mql_root=repo_root/'lab/11_strategy_factory/mql5/Include/AlphaLab/LCM/LCM03'
    forbidden=[]
    for p in mql_root.glob('*'):
        if p.suffix.lower() not in {'.mqh','.mq5'}: continue
        text=p.read_text(encoding='utf-8',errors='ignore')
        for token in ['OrderSend','CTrade','PositionOpen','WebRequest']:
            if re.search(r'\b'+re.escape(token)+r'\b',text): forbidden.append({'path':p.as_posix(),'token':token})
    return {'schema_count':schema_count,'policy_count':len(policies),'forbidden_mql5_hits':forbidden,'passed':not forbidden}
