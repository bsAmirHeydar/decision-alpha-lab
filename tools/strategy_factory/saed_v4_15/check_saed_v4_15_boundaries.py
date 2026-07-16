from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_multimodal_fusion.authority import assert_operation,ALLOWED,FORBIDDEN
from saed_v4_multimodal_fusion.errors import AuthorityError
for op in ALLOWED:assert assert_operation(op)
for op in FORBIDDEN:
 try:assert_operation(op);raise AssertionError(op)
 except AuthorityError:pass
b=json.loads((ROOT/'lab/11_strategy_factory/artifacts/saed_v4_15/AUTHORITY_BOUNDARY.JSON').read_text());assert not b['decision_authority'] and not b['runtime_authority'] and not b['execution_authority'] and not b['attribution_is_causal']
print(f'SAED V4-15 authority boundary passed: {len(ALLOWED)} allowed, {len(FORBIDDEN)} forbidden')
