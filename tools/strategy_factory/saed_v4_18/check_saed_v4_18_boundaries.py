from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_causal_treatment_policy_value.authority import boundary_record,FORBIDDEN
b=boundary_record();assert len(FORBIDDEN)>=10 and all(b[k] is False for k in ['real_causal_claim_authority','production_treatment_ranking_authority','decision_authority','promotion_authority','runtime_authority','execution_authority','production_authority'])
s=json.loads((ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_18.json').read_text(encoding='utf-8'))
assert s['authority']=={k:b[k] for k in s['authority']}
print(f'SAED V4-18 authority boundary passed: {len(b["allowed_operations"])} allowed, {len(b["forbidden_operations"])} forbidden')
