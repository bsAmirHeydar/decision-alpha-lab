#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__);PKG=ROOT/'src/engine/packages/strategy_factory_portfolio_v3';errors=[]
FORBIDDEN=('OrderSend(', 'CTrade', 'PositionOpen(', 'WebRequest(', 'requests.get(', 'requests.post(', 'urllib.request', 'socket.socket', 'subprocess.Popen', 'os.system(', 'eval(', 'exec(')
for p in sorted(PKG.glob('*.py')):
 text=p.read_text(encoding='utf-8')
 for token in FORBIDDEN:
  if token in text:errors.append(f'{p.relative_to(ROOT)} forbidden token {token!r}')
checks={'allocator.py':('ledger.reserve','marginal_risk','max_gross_exposure'),'dependence.py':('fallback_correlation','symbol_correlation','cluster_correlation'),'capacity.py':('expected_fill_ratio','broker_volume_step','impact'),'runtime.py':('order_authority','validation_not_passed','insufficient_contexts'),'reconciliation.py':('missing','extra','mismatch')}
for name,tokens in checks.items():
 text=(PKG/name).read_text()
 for token in tokens:
  if token not in text:errors.append(f'{name} missing {token}')
if errors:print('\n'.join(errors));raise SystemExit(1)
print('UCE-I17 boundary guard: PASS')
