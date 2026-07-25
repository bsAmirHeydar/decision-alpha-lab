from tools.repository_paths import find_repository_root
from pathlib import Path
import ast,json
ROOT=find_repository_root(__file__)
for p in (ROOT/'src/engine/packages/saed_v4_sequence_state_space').glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
for p in (ROOT/'src/engine/packages/saed_v4_sequence_state_space').glob('*.py'):
 t=p.read_text(encoding='utf-8').lower()
 for forbidden in ['order_send(', 'positions_total(', 'trade.mqh', 'mt5.initialize(', 'pickle.loads(', 'eval(', 'exec(']:
  assert forbidden not in t,(p,forbidden)
a=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_12/AUTHORITY_BOUNDARY.JSON').read_text());assert not a['decision_authority'] and not a['runtime_authority'] and not a['execution_authority']
c=json.loads((ROOT/'releases/history/strategy_factory/artifacts/saed_v4_12/CLAIM_LEDGER.JSON').read_text())['claims'];assert not c['real_alpha'] and not c['treatment_selection'] and not c['production_authorization'] and not c['live_trading']
print('V4-12 Python and authority boundaries passed')
