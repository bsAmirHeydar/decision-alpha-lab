from tools.repository_paths import find_repository_root
from pathlib import Path
import sys,json
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from saed_v4_foundation_model_adapters.authority import assert_operation,ALLOWED,FORBIDDEN
from saed_v4_foundation_model_adapters.errors import AuthorityError
for op in ALLOWED:assert assert_operation(op)
for op in FORBIDDEN:
 try:assert_operation(op);raise AssertionError(op)
 except AuthorityError:pass
b=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_14/AUTHORITY_BOUNDARY.JSON').read_text());assert not b['decision_authority'] and not b['runtime_authority'] and not b['execution_authority']
print(f'SAED V4-14 authority boundary passed: {len(ALLOWED)} allowed, {len(FORBIDDEN)} forbidden')
