#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
PKG=ROOT/'src/engine/packages/strategy_factory_policy_v3'
FORBIDDEN=('OrderSend(', 'CTrade', 'PositionOpen(', 'WebRequest(', 'requests.get(', 'requests.post(', 'urllib.request', 'socket.socket', 'subprocess.Popen', 'os.system(', 'eval(', 'exec(')
errors=[]
for p in sorted(PKG.glob('*.py')):
    text=p.read_text(encoding='utf-8')
    for token in FORBIDDEN:
        if token in text: errors.append(f'{p.relative_to(ROOT)} forbidden authority/dynamic token {token!r}')
checks={
 'graph.py':('graph_support_exceeds_promotion','policy_graph_cycle','unreachable_policy_nodes','node_authority_mismatch'),
 'model.py':('STALE_MODEL','OUT_OF_DISTRIBUTION','MISSING_VIEW','UNSUPPORTED_TREATMENT','UNSUPPORTED_RISK'),
 'fallback.py':('FallbackAction.MANUAL_ONLY','FallbackAction.ABSTAIN','FallbackAction.REJECT'),
 'authority.py':('if kill_switch','if risk_rejected','if manual_veto'),
 'engine.py':('DecisionStatus.ABSTAINED','resolve_hard_authority','fallback_resolution')}
for name,tokens in checks.items():
    text=(PKG/name).read_text(encoding='utf-8')
    for token in tokens:
        if token not in text: errors.append(f'{name} missing {token}')
a=(PKG/'authority.py').read_text()
if not a.index('if kill_switch')<a.index('if risk_rejected')<a.index('if manual_veto'):errors.append('hard authority ordering is ambiguous')
if errors: print('\n'.join(errors)); raise SystemExit(1)
print('UCE-I13 boundary guard: PASS')
