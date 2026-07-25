#!/usr/bin/env python3
"""Fail closed if UCE-I12 acquires trading/network authority or hidden-test data access."""
from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
PACKAGE=ROOT/'lab'/'11_strategy_factory'/'python'/'strategy_factory_promotion_v3'
FORBIDDEN=('OrderSend(', 'trade.Buy(', 'trade.Sell(', 'PositionOpen(', 'CTrade', 'requests.get(', 'requests.post(', 'urllib.request', 'socket.socket', 'subprocess.Popen', 'os.system(', 'WebRequest(')
errors=[]
for path in sorted(PACKAGE.glob('*.py')):
    text=path.read_text(encoding='utf-8')
    for token in FORBIDDEN:
        if token in text: errors.append(f'{path.relative_to(ROOT)}: forbidden authority token {token!r}')
for name in ('uncertainty.py','multiplicity.py','winner_overfit.py','nulls.py','stress.py','calibration.py','gate.py'):
    text=(PACKAGE/name).read_text(encoding='utf-8')
    for token in ('load_final_test','read_hidden_test','fetch_final_test'):
        if token in text: errors.append(f'{name}: protected-test access primitive {token!r}')
contracts=(PACKAGE/'contracts.py').read_text(encoding='utf-8')
if 'trial_universe_count_mismatch' not in contracts or 'incomplete_selection_ledger' not in contracts:
    errors.append('complete selection-universe fail-closed checks missing')
gate=(PACKAGE/'gate.py').read_text(encoding='utf-8')
if 'scorecard.critical_blockers' not in gate or 'GateOutcome.REJECT if blockers' not in gate:
    errors.append('non-compensatory critical blocker gate missing')
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print('UCE-I12 boundary guard: PASS')
