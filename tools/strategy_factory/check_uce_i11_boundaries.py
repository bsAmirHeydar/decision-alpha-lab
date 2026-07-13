#!/usr/bin/env python3
"""Fail closed if UCE-I11 acquires execution/network authority or hidden-test coupling."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PACKAGE=ROOT/'lab'/'11_strategy_factory'/'python'/'strategy_factory_experiments_v3'
FORBIDDEN=(
    'OrderSend(', 'trade.Buy(', 'trade.Sell(', 'PositionOpen(', 'CTrade',
    'requests.get(', 'requests.post(', 'urllib.request', 'socket.socket',
    'subprocess.Popen', 'os.system(', 'WebRequest(',
)
errors=[]
for path in sorted(PACKAGE.glob('*.py')):
    text=path.read_text(encoding='utf-8')
    for token in FORBIDDEN:
        if token in text:
            errors.append(f'{path.relative_to(ROOT)}: forbidden authority token {token!r}')
for name in ('search.py','scheduler.py','budget.py','cache.py','isolation.py'):
    text=(PACKAGE/name).read_text(encoding='utf-8')
    for token in ('final_test','hidden_test'):
        if token in text:
            errors.append(f'{name}: search/runtime primitive hardcodes protected role {token!r}')
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print('UCE-I11 boundary guard: PASS')
